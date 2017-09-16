# -*- coding: UTF-8 -*-

#spider of tsxbb.gov.cn
'''
Created on 2015年7月18日

@author: bohaohan
@introduction: spider of tsxbb.gov.cn
'''
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

class tsxbb_Spider(CrawlSpider):
    name = "tsxbb"
    allowed_domains = ["tsxbb.gov.cn"]
    start_urls = ['http://www.tsxbb.gov.cn/zxdt/',
                  'http://www.tsxbb.gov.cn/jdjc/',
                  'http://www.tsxbb.gov.cn/tzgg1/',
                  'http://www.tsxbb.gov.cn/bzgl/',
                  'http://www.tsxbb.gov.cn/sydwgg/',
                  'http://www.tsxbb.gov.cn/zsjs/',
                  'http://www.tsxbb.gov.cn/rdzt/sydwgg/'
    ]


    def parse(self, response):
        '''
        从各个板块获取页数和相应页数的url
        :param response:
        :return:
        '''
        root = bs(response.body)
        te = root.text
        te = te[te.index("var currentPage = ")+16:]
        te = te[:te.index(";")]
        pageText = te
        for i in range(0, int(pageText)):
            if i == 0:
                url = response.url + "index.html"
                yield scrapy.Request(url, self.parse_page,  meta={'forumurl': url})
            else:
                url = response.url + "index_" + str(i) + ".html"
                yield scrapy.Request(url, self.parse_page,  meta={'forumurl': url})

    def parse_page(self, response):
        '''
        从各个页数获取相应新闻页面的url
        :param response:
        :return:
        '''
        root = bs(response.body)
        urls = root.findAll("a", attrs={"href": re.compile("^\./20")})
        forumurl = response.meta['forumurl']
        for url in urls:
            url = url.get("href")
            url = url[1:]
            source = response.url
            source = source[:source.index("index")-1]
            url = source + url
            yield scrapy.Request(url, self.parse_item, meta={'forumurl': forumurl})

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
        item["site_id"] = 13
        item['website_id'] = ''
        item["site_name"] = '通山县机构编制网'
        item["area"] = 958
        item["site_weight"] = 2
        item['countryid'] = 1156
        item['province'] = 1673
        item['city'] = 136
        item["ip"] = socket.gethostbyname("www.tsxbb.gov.cn")
        item["site_url"] = "www.tsxbb.gov.cn"
        item["forumurl"] = response.meta['forumurl']
        item["site_type"] = '新闻'
        item["url"] = response.url
        item["subname"] = root.find("span", attrs={"class": "text14h"}).find("a", attrs={"href": "../"}).text
        item["title"] = root.find("td", attrs={"class": "textbiaoti"}).text
        str = root.find("td", attrs={"class": "text12hui"}).text
        str = str[str.index('20'):]
        item["pubdate"] = str[:str.index('&nbsp;')-1]
        try:
            str = str[str.index('su = ')+6:]
            item["website_id"] = str[:str.index(';')-1]
        except:
            item["website_id"] = ""
        styles = root.find("div", attrs={"class": "TRS_Editor"}).findAll("style")
        for style in styles:
            style.clear()
        #替换所有图片标签
        imgs = root.find("div", attrs={"class": "TRS_Editor"}).findAll("img")
        for img in imgs:
            img.replaceWith(img.prettify())

        item["txt"] = root.find("div", attrs={"class": "TRS_Editor"}).text.replace("\r\n", "$*huanhang*$").replace("\n", "$*huanhang*$").replace("\"", "'").replace("<br />", "$*huanhang*$")
        item["txt_len"] = len(item["txt"])
        item["domain_1"] = "tsxbb.gov.cn"
        item["domain_2"] = "www"
        item["snatch_time"] = datetime.datetime.now()
        return item