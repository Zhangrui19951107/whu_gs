# -*- coding: UTF-8 -*-

#spider of tsxbb.gov.cn
'''
Created on 2015年7月18日

@author: bohaohan
@introduction: spider of tsxbb.gov.cn
'''
import codecs
import re
import datetime
import socket

__author__ = 'bohaohan'

import scrapy
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from BeautifulSoup import BeautifulSoup as bs
from fenghuo.items import FenghuoItem
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
t_url = set([])



class tsxbb_Spider(CrawlSpider):
    name = "jlxbbt"
    allowed_domains = ["jlxbb.gov.cn"]
    start_urls = ['http://www.jlxbb.gov.cn/zxdt/',
                  'http://www.jlxbb.gov.cn/jdjc/',
                  'http://www.jlxbb.gov.cn/tzgg/',
                  'http://www.jlxbb.gov.cn/tzgg1/',
                  'http://www.jlxbb.gov.cn/bzgl/',
                  'http://www.jlxbb.gov.cn/sydwgg/',
                  'http://www.jlxbb.gov.cn/zsjs/',
                  'http://www.jlxbb.gov.cn/rdzt/sydwgg/'
    ]


    def parse(self, response):
        '''
        从各个板块获取页数和相应页数的url
        :param response:
        :return:
        '''
        if response.status == 404:
            self.log('Hi, this is an 404 page! %s' % response.url)
            pass
        url = response.url
        yield scrapy.Request(url, self.parse_page,  meta={'forumurl': url})
        # root = bs(response.body)
        # te = root.text
        # te = te[te.index("var currentPage = ")+16:]
        # te = te[:te.index(";")]
        # pageText = te
        # for i in range(0, int(pageText)):
        #     if i == 0:
        #         url = response.url + "index.html"
        #         yield scrapy.Request(url, self.parse_page,  meta={'forumurl': url})
        #     else:
        #         url = response.url + "index_" + str(i) + ".html"
        #         yield scrapy.Request(url, self.parse_page,  meta={'forumurl': url})

    def parse_page(self, response):
        '''
        从各个页数获取相应新闻页面的url
        :param response:
        :return:
        '''
        self.log('Hi, this is an parse_page! %s' % response.url)
        forumurl = response.meta['forumurl']
        url = response.url
        new = 2
        l_time = "0" # 最后一次爬取时间
        while new > 1:
            new = 0
            r = requests.get(url)
            r.encoding = "utf-8"

            root = bs(r.text.decode("utf-8"))
            tables = root.findAll("table", attrs={"width": "96%"})
            for table in tables:
                time = table.find("td", attrs={"align": "right"}).text
                time = time[1:time.index("]")]
                year = time[:time.index("年")]
                month = time[time.index("年") + 1: time.index("月")]
                day = time[time.index("月") + 1: time.index("日")]
                time = year + "-" + month + "-" + day
                if time > l_time:
                    new += 1
                    curl = table.find("a", attrs={"href": re.compile("^\./20")})
                    curl = curl.get("href")
                    curl = curl[2:]
                    source = response.url
                    curl = source + curl
                    #print curl
                    yield scrapy.Request(curl, self.parse_item, meta={'forumurl': forumurl})
            #div = root.find("div", attrs={"class": "fenye"})
            curls = root.findAll("a")
            hasNext = False
            for urls in curls:
                if urls.text == "下一页":
                    url = urls.get("href")
                    hasNext = True
            if not hasNext:
                break


    def parse_item(self, response):
        '''
        访问各新闻页面，获取各键值
        :param response:
        :return:
        '''
        self.log('Hi, this is an item page! %s' % response.url)
        item = FenghuoItem()
        root = bs(response.body)
        item['topPost'] = 1
        item["site_id"] = 28
        item['website_id'] = ''
        item["site_name"] = '江陵县机构编制网'
        item["area"] = 2550
        item["site_weight"] = 2
        item['countryid'] = 1156
        item['province'] = 1673
        item['city'] = 136
        item["ip"] = socket.gethostbyname("www.jlxbb.gov.cn")
        item["site_url"] = "www.jlxbb.gov.cn"
        item["forumurl"] = response.meta['forumurl']
        item["site_type"] = '新闻'
        item["url"] = response.url
        try:
            item["subname"] = root.find("span", attrs={"class": "text14h"}).find("a", attrs={"href": "../"}).text
            item["title"] = root.find("td", attrs={"class": "textbiaoti"}).text
            str = root.find("td", attrs={"class": "text12hui"}).text
            str = str[str.index('20'):]
            item["pubdate"] = str[:str.index('&nbsp;')-1]
            try:
                str = str[str.index('su = ')+6:]
                item["website_name"] = str[:str.index(';')-1]
            except:
                item["website_name"] = ""
            styles = root.find("div", attrs={"class": "TRS_Editor"}).findAll("style")
            for style in styles:
                style.clear()
            #替换所有图片标签
            imgs = root.find("div", attrs={"class": "TRS_Editor"}).findAll("img")
            for img in imgs:
                img.replaceWith(img.prettify())

            item["txt"] = root.find("div", attrs={"class": "TRS_Editor"}).text.replace("\r\n", "$*huanhang*$").replace("\n", "$*huanhang*$").replace("\"", "'").replace("<br />", "$*huanhang*$")
            item["txt_len"] = len(item["txt"])
            item["domain_1"] = "jlxbb.gov.cn"
            item["domain_2"] = "www"
            item["snatch_time"] = datetime.datetime.now()

            return item
        except:
            line = response.url + "\n"
            self.file = codecs.open('error2.json', 'ab', encoding='utf-8')
            self.file.write(line.decode("unicode_escape"))
            pass