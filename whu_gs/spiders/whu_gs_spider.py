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


class whu_gs_spider(CrawlSpider):
    name = "whu_gs_spider"
    allowed_domains = ["gs.whu.edu.cn"]

    start_urls = [
        'http://www.gs.whu.edu.cn/index.php/index-show-tid-40-p-1.html'
    ]
    new = 11
    total_new = 0
    url = start_urls[0]
    hasNext = True
    now = datetime.date.today()
    delay = datetime.timedelta(days=150)
    pages = 1
    isFirst = True
    def parse(self, response):
        '''

        :param response:
        :return:

        取各版块的url并传入到parse_pages

        '''
        #test
        # url = 'http://www.gs.whu.edu.cn/index.php/index-show-tid-40-p-1.html'
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
        div = root.find("div", attrs={"class": "ulnotice"})
        lis = div.findAll("li")
        for li in lis:
            item = FenghuoItem()
            iurl = li.find("a").get("href")
            if iurl[0:4]!='http':
                iurl='http://gs.whu.edu.cn'+iurl
            title = li.find("a").text
            pubdate = li.find("span").text
            month = pubdate[6:8]
            day = pubdate[9:11]
            hour = '00'
            year = pubdate[1:5]
            item_date = datetime.date(int(year), int(month), int(day))
            if (not updatetool.hasUrl(iurl)) and self.now - item_date < self.delay:
                self.new += 1
                self.total_new += 1
                yield scrapy.Request(iurl, self.parse_items)#according to iurl,requuest the detail page
        url = 'http://www.gs.whu.edu.cn/index.php/index-show-tid-40-p-'+str(self.pages)+'.html'
        if self.new > 10 and self.hasNext:
            yield scrapy.Request(url, self.parse)
        else:
            line = str(datetime.datetime.now()) + " Totally crawled " + str(self.total_new) + " items " + self.name + " spider has finished start!\n\n"
            t_file.write(line.decode("unicode_escape"))
    def parse_items(self,response):

        #title done
        #txt:main work,focus on parse HTML and remove impurity
        #pubdate done
        #snatch_time static
        #site_url static
        #site_name static
        #url done
        #topPost static
        #url done

        #init:
        html_parser = HTMLParser.HTMLParser()
        item = FenghuoItem()
        url = response.url

        self.log("Hi,this is in parse_items,url is %s" % url)
        root = bs(response.body)
        div=root.find("div","ny_con news_con_ny")
        pubdate0 = div.find("p","news_time").text
        year=pubdate0[3:7]
        month=pubdate0[8:10]
        day=pubdate0[11:13]
        hour='00'
        pubdate=str(year) + "-" + month + "-" + day + " " + hour + ":00"
        ps = div.findAll("p","MsoNormal")
        title = div.find("h3").text
        html = ""
        #see if there's rubbish in ps remove:
        print ps[-1]
        if ps[-1].find("div","page"):
            del ps[-1]
        print 'sssssssssssssss'
        # get txt by paragraph
        for p in ps:
            #remove comments in text:
            comments = p.findAll(text=lambda text:isinstance(text,Comment))
            [comment.extract() for comment in comments]
            html = html + '\n' + p.text.encode('utf-8')
        text = html_parser.unescape(html)
        item['url'] = url
        item['title'] = html_parser.unescape(title)
        item['txt'] = text
        item['pubdate'] = str(pubdate)
        item['snatch_time'] = datetime.datetime.now()
        item['topPost'] = 1
        item['site_name'] = '武汉大学研究生院'
        item['site_url'] = "www.gs.whu.edu.cn/"
        f=open('scrapy_log.txt','a')
        f.write(html_parser.unescape(title)+'\n'+str(pubdate)+'\n')
        f.close()
        fp.process_item(item, "123")