# coding=utf-8
import ConfigParser

from scrapy.core.downloader import Downloader
from scrapy.utils.defer import mustbe_deferred
import time
import warnings
from scrapy import signals
from scrapy.core.downloader import Slot
import logging
import codecs
from scrapy.core.downloader.middleware import DownloaderMiddlewareManager
from scrapy.core.downloader.handlers import DownloadHandlers
from twisted.internet import task, reactor, defer
import datetime
import MySQLdb
from collections import deque

import DefaultInfo
from allocate import *
import random
import sites as sas

logger = logging.getLogger("MainCrawler")


def singleton1(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton1
class logfile():
    def log(self, info):
        file_name = DefaultInfo.HOME_DIR + "/log/request_log/log-" + str(datetime.date.today()) + ".txt"
        t_file = codecs.open(file_name, 'a', encoding='utf-8')
        line = str(datetime.datetime.now()) + " " + info + "\n"
        t_file.write(line)


class Slot(object):
    """Downloader slot"""

    def __init__(self, concurrency, delay, settings):
        self.concurrency = concurrency
        self.delay = delay
        self.randomize_delay = settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
        self.active = set()
        self.queue = deque()
        self.transferring = set()
        self.lastseen = 0
        self.latercall = None

    def free_transfer_slots(self):
        return self.concurrency - len(self.transferring)

    def download_delay(self):
        if self.randomize_delay:
            return random.uniform(0.5 * self.delay, 1.5 * self.delay)
        return self.delay

    def close(self):
        if self.latercall and self.latercall.active():
            self.latercall.cancel()


def _get_concurrency_delay(concurrency, spider, settings):
    delay = settings.getfloat('DOWNLOAD_DELAY')
    if hasattr(spider, 'DOWNLOAD_DELAY'):
        warnings.warn("%s.DOWNLOAD_DELAY attribute is deprecated, use %s.download_delay instead" %
                      (type(spider).__name__, type(spider).__name__))
        delay = spider.DOWNLOAD_DELAY
    if hasattr(spider, 'download_delay'):
        delay = spider.download_delay
    if hasattr(spider, 'max_concurrent_requests'):
        concurrency = spider.max_concurrent_requests
    return concurrency, delay


def singleton(cls):
    instances = {}

    def _singleton(crawler):
        if cls not in instances:
            instances[cls] = cls(crawler)
        else:
            instances[cls].add_crawler(crawler)
        return instances[cls]

    return _singleton


class pack_dict(object):
    m_logger = logging.getLogger("downloader dict")

    def __init__(self):
        self._index = dict()

    def __getitem__(self, item):
        if item not in self._index.keys():
            self._index[item] = set()
        return self._index[item]

    def __len__(self):
        length = 0
        for _set in self._index.values():
            length += len(_set)
        return length

    def __str__(self):
        str = "["
        for k, v in self._index.items():
            str += k + ": ("
            for item in v:
                str += item + ", "
            str += "), "
        str += "]"
        return str

    def __delitem__(self, key):
        if len(self._index[key]) > 0:
            self._index[key].clear()
        del self._index[key]

    def __call__(self, spider):
        return len(self._index[spider.name]) > 0

    def print_use(self):
        for k, v in self._index.items():
            logfile().log("spider " + k + " has " + str(len(v)) + " active request")


conf = ConfigParser.ConfigParser()
conf.read(DefaultInfo.HOME_DIR + "/db.cfg")


def getConn():
    return MySQLdb.connect(host=conf.get("mysql", "ip"), user=conf.get("mysql", "user"),
                           passwd=conf.get("mysql", "pwd"), charset='utf8')


def closeConn(conn):
    if conn:
        conn.close()


@singleton
class MDownloader(Downloader):
    pretime = time.time()

    def __init__(self, crawler):
        logger.debug(crawler.spider.name + " call the downloader")
        self.settings = dict()
        self.settings[crawler.spider.name] = crawler.settings
        self.signals = dict()
        self.signals[crawler.spider.name] = crawler.signals
        self.slots = {}
        self.conn = getConn()
        cur = self.conn.cursor()
        self.conn.select_db(conf.get("mysql", "db"))
        self.conn.commit()
        cur.close()
        self.actives = pack_dict()
        self.handlers = dict()
        self.handlers[crawler.spider.name] = DownloadHandlers(crawler)
        self.total_concurrency = self.settings[crawler.spider.name].getint('CONCURRENT_REQUESTS')
        self.domain_concurrency = self.settings[crawler.spider.name].getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        self.ip_concurrency = self.settings[crawler.spider.name].getint('CONCURRENT_REQUESTS_PER_IP')
        self.middleware = dict()
        self.middleware[crawler.spider.name] = DownloaderMiddlewareManager.from_crawler(crawler)
        self._slot_gc_loop = task.LoopingCall(self._slot_gc)
        self._slot_gc_loop.start(60)
        self.rememberseq = dict()
        self.wastedtime = 0
        mlist = self.settings[crawler.spider.name].get("TO_CHANGE")
        if mlist is not None:
            logger.debug("getIt~!!")
            DefaultInfo.printinfo(mlist)
            self.rememberseq = mlist
            out = ""
            for k in mlist.keys():
                out += k + ":" + str(mlist[k]) + ":"
            self.insert_end("", out, str(datetime.datetime.now()))

        propor_dict = self.settings[crawler.spider.name].get("SPIDER_PROPORTION")
        if propor_dict is not None:
            logger.debug("get proportion dict " + str(propor_dict))
            self.proportion_dict = propor_dict

    def __del__(self):
        if self.conn:
            closeConn(self.conn)

    '''
        获取爬虫对应的最大同时下载数
    '''

    def _get_concurrency(self, spider):
        if self._get_slot_key(spider=spider) in self.slots.keys():
            logfile().log(
                spider.name + " has key and is " + str(self.slots[self._get_slot_key(spider=spider)].concurrency))
            return self.slots[self._get_slot_key(spider=spider)].concurrency
        if self.rememberseq.__sizeof__() != 0 and spider.name in self.rememberseq.keys():
            return self.rememberseq[spider.name]
        if hasattr(spider, 'max_concurrent_requests'):
            return spider.max_concurrent_requests
        return self.ip_concurrency if self.ip_concurrency else self.domain_concurrency

    '''
        该爬虫是否需要等待
    '''

    def needs_backout(self, spider):
        return len(self.actives[spider.name]) >= 2 * self._get_concurrency(spider) or len(
            self.actives) >= 2 * self.total_concurrency

    def add_crawler(self, crawler):
        self.settings[crawler.spider.name] = crawler.settings
        self.signals[crawler.spider.name] = crawler.signals
        self.handlers[crawler.spider.name] = DownloadHandlers(crawler)
        self.middleware[crawler.spider.name] = DownloaderMiddlewareManager.from_crawler(crawler)

    def _get_slot(self, request=None, spider=None):
        key = self._get_slot_key(request, spider)
        if key not in self.slots.keys():
            conc = self.ip_concurrency if self.ip_concurrency else self.domain_concurrency
            conc, delay = _get_concurrency_delay(conc, spider, self.settings[spider.name])
            self.slots[key] = Slot(conc, delay, self.settings[spider.name])
            if self.rememberseq.__sizeof__() != 0 and spider.name in self.rememberseq.keys():
                logger.info("change it!")
                self.slots[key].concurrency = self.rememberseq[spider.name]
                del self.rememberseq[spider.name]
            else:
                logger.info("nothing")
        return key, self.slots[key]

    def _get_slot_key(self, request=None, spider=None, spidername=None):
        if request is not None and 'download_slot' in request.meta:
            return request.meta['download_slot']
        if spidername is not None:
            return spidername + '_slot'
        return spider.name + '_slot'

    def change_slot_concurrent(self, spider=None, spidername=None, newsize=16):
        if spidername is not None:
            key = self._get_slot_key(spidername=spidername)
        else:
            key = self._get_slot_key(spider=spider)
        DefaultInfo.printinfo(key)
        logger.info("change IT!!!!!!!!!")
        self.slots[key].concurrency = newsize
        DefaultInfo.printinfo(self.slots[key])

    def fetch(self, request, spider):
        def _deactivate(response):
            self.actives[spider.name].remove(request)
            self.actives.print_use()
            return response

        self.actives[spider.name].add(request)
        self.actives.print_use()
        dfd = self.middleware[spider.name].download(self._enqueue_request, request, spider)
        return dfd.addBoth(_deactivate)

    def _enqueue_request(self, request, spider):
        key, slot = self._get_slot(request, spider)
        request.meta['download_slot'] = key

        def _deactivate(response):
            slot.active.remove(request)
            return response

        slot.active.add(request)
        deferred = defer.Deferred().addBoth(_deactivate)
        slot.queue.append((request, deferred))
        self._process_queue(spider, slot)
        return deferred

    def _process_queue(self, spider, slot):
        if slot.latercall and slot.latercall.active():
            return

        # Delay queue processing if a download_delay is configured
        now = time.time()
        delay = slot.download_delay()
        if delay:
            penalty = delay - now + slot.lastseen
            if penalty > 0:
                slot.latercall = reactor.callLater(penalty, self._process_queue, spider, slot)
                return

        # Process enqueued requests if there are free slots to transfer for this slot
        while slot.queue and slot.free_transfer_slots() > 0:
            slot.lastseen = now
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request, spider)
            dfd.chainDeferred(deferred)
            # prevent burst if inter-request delays were configured
            if delay:
                self._process_queue(spider, slot)
                break

    def _download(self, slot, request, spider):
        # The order is very important for the following deferreds. Do not change!

        request.meta['the_id_from_scrapy'] = 0

        # 1. Create the download deferred

        def download_request(request, spider):
            starttime = str(datetime.datetime.now())
            request.meta['the_id_from_scrapy'] = self.write_database_start(spider.name, starttime)
            return self.handlers[spider.name].download_request(request, spider)

        dfd = mustbe_deferred(download_request, request, spider)

        # 2. Notify response_downloaded listeners about the recent download
        # before querying queue for next request
        def _downloaded(response):
            size = len(str(response.body))
            self.write_database_end(request.meta['the_id_from_scrapy'], str(datetime.datetime.now()), size)
            self.signals[spider.name].send_catch_log(signal=signals.response_downloaded,
                                                     response=response,
                                                     request=request,
                                                     spider=spider)
            return response

        dfd.addCallback(_downloaded)

        def _err_handle(response):
            self.delete_bad_with_id(request.meta['the_id_from_scrapy'])
            return response

        dfd.addErrback(_err_handle)
        # 3. After response arrives,  remove the request from transferring
        # state to free up the transferring slot so it can be used by the
        # following requests (perhaps those which came from the downloader
        # middleware itself)
        slot.transferring.add(request)

        def finish_transferring(_):
            slot.transferring.remove(request)
            self._process_queue(spider, slot)
            return _

        return dfd.addBoth(finish_transferring)

    def write_database_start(self, spider_name, start_time):
        cur = self.conn.cursor()
        cur.execute("insert into request_log(spider_name, start_time) values(%s, %s)", (spider_name, start_time))
        self.conn.commit()
        DefaultInfo.printinfo("4544444444444444444")
        cur.execute("select id from request_log where start_time = %s and spider_name = %s", (start_time, spider_name))
        DefaultInfo.printinfo("6666666666666666666")
        the_id = 0
        for _id in cur.fetchall():
            the_id = _id[0]
        DefaultInfo.printinfo("333333333333333333")
        # self.conn.commit()
        cur.close()
        DefaultInfo.printinfo("333333333333333333")
        DefaultInfo.printinfo(the_id)
        return the_id

    def delete_bad_with_id(self, _id):
        cur = self.conn.cursor()
        cur.execute("delete from request_log where id = %s", (_id,))
        self.conn.commit()
        cur.close()

    def write_database_end(self, _id, end_time, size):
        cur = self.conn.cursor()
        DefaultInfo.printinfo(str(_id) + ' write end')
        cur.execute("update request_log set end_time = %s, response_size = %s where id = %s",
                    (end_time, str(size), _id))
        self.conn.commit()
        cur.close()

    def stop_spider(self, spidername):
        del self.settings[spidername]
        del self.signals[spidername]
        del self.handlers[spidername]
        del self.middleware[spidername]
        del self.actives[spidername]
        self.slots[self._get_slot_key(spidername=spidername)].close()
        self.slots[self._get_slot_key(spidername=spidername)].active = None
        self.slots.pop(self._get_slot_key(spidername=spidername))
        logger.debug(spidername + " stop its slot & slost is " + str(len(self.slots)))
        self.reset_concurrency(spidername)
        self.delete_bad_record(spidername)

    def delete_bad_record(self, spidername):
        cur = self.conn.cursor()
        cur.execute("delete from request_log where spider_name = %s and end_time is NULL", (spidername,))
        DefaultInfo.printinfo("delete bad record of " + spidername)
        self.conn.commit()
        cur.close()

    def reset_concurrency(self, spidername):
        for site in sas.sitelist:
            if site.crawlername == spidername:
                site.inuse = 0
                site.v = 0
                site.pr()
        sas.sitelist = allocate(sitelist=sas.sitelist, interval=20, U=self.total_concurrency)
        DefaultInfo.printinfo('111111111111111111111111111111111111')
        info = ""
        for site in sas.sitelist:
            if site.inuse != 0:
                self.change_slot_concurrent(spidername=site.crawlername, newsize=site.v)
                info += site.crawlername + ":" + str(site.v) + ':'
                site.pr()
                DefaultInfo.printinfo('22222222222222222222222222222222222')
        self.insert_end(spidername, info, str(datetime.datetime.now()))

        # if self.total_concurrency is not None:
        #     total_concurrency = self.total_concurrency
        #     current_key = [x for x in self.proportion_dict.keys() if self._get_slot_key(spidername=x) in self.slots.keys()]
        #     DefaultInfo.printinfo(current_key
        #     all_sum = 0
        #     for key in current_key:
        #         all_sum += self.proportion_dict[key]
        #     DefaultInfo.printinfo(all_sum
        #     for key in current_key:
        #         self.change_slot_concurrent(spidername=key, newsize=int(self.proportion_dict[key] / float(all_sum) *
        #                                                                 total_concurrency))

    def insert_end(self, spidername, info, time):
        cur = self.conn.cursor()
        cur.execute("insert into end_allocate_log(spider_name, allocate_time, allocate_info) values(%s, %s, %s)",
                    (spidername, time, info))
        self.conn.commit()
        cur.close()

    def close(self):
        self._slot_gc_loop.stop()

    def _slot_gc(self, age=60):
        mintime = time.time() - age
        if len(self.slots) <= 0:
            self.close()
        for key, slot in self.slots.items():
            if not slot.active and slot.lastseen + slot.delay < mintime:
                self.slots.pop(key).close()
