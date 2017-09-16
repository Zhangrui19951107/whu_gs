# -*- coding: UTF-8 -*-
#spider of huanqiu_domesticnews
'''
Created on 2015年11月26日
@author: zhuwenpeng
@introduction: spider of http://china.huanqiu.com/local/index.html
'''
import codecs
import re
import datetime
import socket
import HTMLParser#used to parse HTML

__author__ = 'zhuwenpeng'
import scrapy
from scrapy.spiders import CrawlSpider
from BeautifulSoup import BeautifulSoup as bs
from BeautifulSoup import Comment#used to remove comments in text
from fenghuo.items import FenghuoItem
import requests
import datetime
from com.crawler.dao.UpdateTool import UpdateTool
from fenghuo.pipelines import FenghuoPipeline as FP
fp = FP()
root_domain = "http://china.huanqiu.com/"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class HuanqiuSpider(CrawlSpider):

    name = "huanqiu_domesticnews_item"
    start_urls = [
        'http://china.huanqiu.com/local/index.html'
    ]
    new = 11
    total_new = 0
    url = start_urls[0]
    hasNext = True
    now = datetime.date.today()
    delay = datetime.timedelta(days=3)
    pages = 1
    isFirst = True

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
        div=root.find("div","conText")
        strong1= div.find("strong","fromSummary")
        pubdate = div.find("strong","timeSummary").text
        ps = div.find("div",attrs={"id":"text"}).findAll("p")
        item_page = div.find("div",attrs={"id":"pages"})
        title = div.find("h1").text
        html = ""
        #see if there's rubbish in ps remove:
        print ps[-1]
        if ps[-1].find("div","page"):
            del ps[-1]
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
        item['site_name'] = '环球国内新闻'
        item['site_url'] = "china.huanqiu.com/"
        # see if the txt of this page has a next page 
        if item_page:
            next_page = item_page.findAll("a")
            for a in next_page:
                if a.text == "下一页":
                    next_url = a.get('href') # get the next page
        else:
            fp.process_item(item, "123") #all txt in a single page ,just process item to DB

        if next_url == url: 
                 #means we are parsing the last page  of the whole txt    
                 print next_url
        else:
            #means we stiill has a next page to request to get the remaining part of the txt
            yield scrapy.Request(url=next_url, meta={'item': item},callback=self.parse_items_page)     
            #choose parse_items_page to parse ,pass item with meta                               

    def parse_items_page(self,response):
        #init:
        html_parser = HTMLParser.HTMLParser()
        url = response.url

        self.log("Hi,this is in parse_items_page,url is %s" % url)       
        item = response.meta['item']
        root = bs(response.body)
        div=root.find("div","conText")
        ps = div.find("div",attrs={"id":"text"}).findAll("p")
        item_page = div.find("div",attrs={"id":"pages"})
        html = ""
        print ps[-1]
        if ps[-1].find("div","page"):
            del ps[-1]
        print 'sssssssssssssss'
        for p in ps:
            comments = p.findAll(text=lambda text:isinstance(text,Comment))
            [comment.extract() for comment in comments] 
            html = html+'\n' + p.text.encode('utf-8')
        text = html_parser.unescape(html)
        item['txt'] = item['txt']  + '\n' + text
        next_page = item_page.findAll("a")
        print next_page
        for a in next_page:
             if a.text == "下一页":
                 next_url = a.get('href')
                 print next_url
        if next_url == url: 
            print item['txt']
             #means we are parsing the last page,all parts of the txt has been put into item.
            fp.process_item(item, "123")          
        else:
            yield scrapy.Request(url=next_url, meta={'item': item},callback=self.parse_items_page)                       
             #choose parse_items_page to parse ,pass item with meta

    def parse(self, response):
        
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
        root = bs(response.body)
        div = root.find("div","fallsFlow")
        lis = div.findAll("li")
        for li in lis:
            iurl = li.find("a").get("href")
            pubdate = li.find("h6").text
            year = pubdate[0:4]
            month = pubdate[5:7]
            day = pubdate[8:10]
            item_date = datetime.date(int(year), int(month), int(day))

            yield scrapy.Request(iurl, self.parse_items)#according to iurl,requuest the detail page

            if (not updatetool.hasUrl(iurl)) and self.now - item_date < self.delay:
                self.new += 1
                self.total_new += 1
        if self.pages>=2:
           url = 'http://china.huanqiu.com/local/'+str(self.pages)+'.html'
        else:
            url = 'http://china.huanqiu.com/local/index.html'
        if self.new > 10 and self.hasNext:
            yield scrapy.Request(self.url, self.parse)
        else:
           line = str(datetime.datetime.now()) + " Totally crawled " + str(self.total_new) + " items " + self.name + " spider has finished start!\n\n"
           t_file.write(line.decode("unicode_escape"))
       