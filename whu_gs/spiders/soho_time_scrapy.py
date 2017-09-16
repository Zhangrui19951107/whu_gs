# -*- coding: UTF-8 -*-

#spider of sina news
'''
Created on 2015年10月2日

@author: cly
@introduction: spider of http://news.sohu.com/guoneixinwen.shtml
'''
import codecs
import re
import datetime
import socket

__author__ = 'cly'
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from BeautifulSoup import BeautifulSoup as bs
from BeautifulSoup import Comment#used to remove comments in text
from fenghuo.items import FenghuoItem
import HTMLParser#used to parse HTML
import requests
from com.crawler.dao.UpdateTool import UpdateTool
import datetime, calendar

root_domain = "http://news.sohu.com/"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from fenghuo.pipelines import FenghuoPipeline as FP
fp = FP()
updatetool = UpdateTool()

class SoHuSpider(CrawlSpider):
    name = "sohus"
    allowed_domains = ["news.sohu.com"]

    start_urls = [

        'http://news.sohu.com/guoneixinwen.shtml'
    ]
    new = 11
    total_new = 0
    url = start_urls[0]
    hasNext = True
    now = datetime.date.today()
    delay = datetime.timedelta(days=3)
    pages = 1
    isFirst = True

    def parse(self, response):
        '''

        :param response:
        :return:

        取出新闻页面的具体信息

        '''
        #test
        # url = 'http://www.xcxww.com/content-19-3751-1.html'
        # yield scrapy.Request(url, self.parse_item)
        #end test
        self.log('Hi, this is an page! %s' % response.url)
        file_name = "log-" + str(datetime.date.today()) + ".txt"
        t_file = codecs.open(file_name,'ab',encoding='utf-8')
        if self.isFirst:
            self.isFirst = False
            line = str(datetime.datetime.now()) + " " + self.name + " spider has started!\n"
            t_file.write(line.decode("unicode_escape"))

        updatetool = UpdateTool()
        self.log('Hi, this is an page! %s' % response.url)
       
        self.new = 0
        self.pages += 1
        root = bs(response.body.decode('gb2312'))
        codeTexts = root.find("script",attrs={"language":"JavaScript"}).text


        maxPage = codeTexts[codeTexts.index("maxPage")+10:codeTexts.index("maxPage")+14]

        # maxPage = int(maxPage)
        #print maxPage
        div = root.find("div", attrs={"class": "new-article"})
        lis = div.findAll("div", attrs={"class": "article-list"})

        for li in lis:
            iurl = li.find("h3").contents[1].get("href")
            title = li.find("h3").contents[1].text
            pubdate = li.find("div", attrs={"class": "time"}).text
            pubdate = pubdate[pubdate.index(" ")+1:]
            year = pubdate[0:4]
            month = pubdate[5:7]
            day = pubdate[8:10]
            item_date = datetime.date(int(year), int(month), int(day))
            yield scrapy.Request(iurl, self.parse_items)#according to iurl,requuest the detail page
            if (not updatetool.hasUrl(iurl)) and self.now - item_date < self.delay:
                self.new += 1
                self.total_new += 1

        url = 'http://news.sohu.com/guoneixinwen_'+str(maxPage-self.pages+1)+'.shtml'
        print url
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
        div=root.find("div","content-box clear")
        pubdate0 = div.find("div","time").text
        year=pubdate0[0:4]
        month=pubdate0[5:7]
        day=pubdate0[8:10]
        hour=pubdate0[11:13]
        minute=pubdate0[14:16]
        pubdate=str(year) + "-" + month + "-" + day + " " + hour + ":"+minute
        ps = div.findAll("p")
        title = div.find("h1").text
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
        item['site_name'] = '搜狐国内新闻'
        item['site_url'] = "news.sohus.com/"
        # see if the txt of this page has a next page
        fp.process_item(item, "123")