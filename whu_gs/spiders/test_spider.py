# -*- coding: UTF-8 -*-

#spider of whu gs
'''
Created on 2015年11月16日

@author: zhangrui
@introduction: spider of http://www.gs.whu.edu.cn/index.php/index-show-tid-40-p-1.html
'''
import codecs
import re
import datetime
import socket
import HTMLParser#used to parse HTML

__author__ = 'zhangrui'
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from BeautifulSoup import BeautifulSoup as bs
from BeautifulSoup import Comment#used to remove comments in text
from fenghuo.items import FenghuoItem
import requests
from com.crawler.dao.UpdateTool import UpdateTool
import datetime, calendar


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from fenghuo.pipelines import FenghuoPipeline as FP
fp = FP()


class test_spider(CrawlSpider):
    name = "test_spider"
    allowed_domains = ["sohu.com"]

    start_urls = [
        'http://m.sohu.com/cl/58/?page=1'
    ]
    new = 11
    total_new = 0
    url = start_urls[0]
    hasNext = True
    now = datetime.date.today()
    delay = datetime.timedelta(days=30)
    pages = 1
    isFirst = True
    def parse(self, response):
        '''

        :param response:
        :return:

        取各版块的url并传入到parse_pages

        '''
        #test
        # url = 'http://m.sohu.com/cl/58/?page=1'
        # yield scrapy.Request(url, self.parse_item)
        #end test
        file_name = "log-" + str(datetime.date.today()) + ".txt"
        t_file = codecs.open(file_name, 'ab', encoding='utf-8')
        if self.isFirst:
            self.isFirst = False
            line = str(datetime.datetime.now()) + " " + self.name + " spider start!\n"
            t_file.write(line.decode("unicode_escape"))

        updatetool = UpdateTool()
        self.log('Hi, this is an page! %s' % response.url)
        self.new = 0
        self.pages += 1
        root = bs(response.body.decode('utf-8'))
        div = root.find("div", attrs={"class": "bd3 pb1"})
        lis = div.findAll("p")
        for li in lis:
            item = FenghuoItem()
            iurl = 'm.sohu.com'+li.find("a").get("href")
            title = li.find("a").text
            pubdate = root.find('p',attrs={'class': 'w c2'}).text
            month = pubdate[16:18]
            day = pubdate[19:21]
            hour = pubdate[22:24]
            year = pubdate[11:15]
            item_date = datetime.date(int(year), int(month), int(day))
            item['url'] = iurl
            item['title'] = title
            item['pubdate'] = str(item_date)
            item['snatch_time'] = datetime.datetime.now()
            item['topPost'] = 1
            item['site_name'] = '手机搜狐网'
            item['site_url'] = "m.sohu.com/"
            print item
            if (not updatetool.hasUrl(iurl)) and self.now - item_date < self.delay:
                self.new += 1
                self.total_new += 1
                fp.process_item(item, "123")
        url = 'http://m.sohu.com/cl/58/?page='+str(self.pages)
        if self.new > 3 and self.hasNext:
            yield scrapy.Request(url, self.parse)
        else:
            line = str(datetime.datetime.now()) + " Totally crawled " + str(self.total_new) + " items " + self.name + " spider has finished start!\n\n"
            t_file.write(line.decode("unicode_escape"))
