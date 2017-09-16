# -*- coding: UTF-8 -*-

#spider of cntongshan.com
'''
Created on 2015年7月30日

@author: bohaohan
@introduction: spider of http://www.xfxc.gov.cn/ 襄城区人民政府
'''
import codecs
import re
import datetime
import socket

__author__ = 'bohaohan'
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from BeautifulSoup import BeautifulSoup as bs
from fenghuo.items import FenghuoItem
import requests

root_domain = "http://www.xfxc.gov.cn/"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class TongShanChinaSpider(CrawlSpider):
    name = "xfxc"
    allowed_domains = ["xfxc.gov.cn"]

    start_urls = [
        'http://www.xfxc.gov.cn/list-6-1.html'
    ]

    def parse(self, response):
        '''

        :param response:
        :return:

        取各版块的url并传入到parse_pages

        '''
        #test
        # url = 'http://www.xcxww.com/content-19-3751-1.html'
        # yield scrapy.Request(url, self.parse_item)
        #end test

        self.log('Hi, this is an page! %s' % response.url)
        url_set = set([])
        new = 21
        url = response.url
        hasNext = True
        while new > 10 and hasNext:
            self.log('Hi, this is an page! %s' % url)
            new = 0
            hasNext = False
            r = requests.get(url)
            r.encoding = 'gb2312'
            root = bs(r.text)
            div = root.find("div", attrs={"class": "tabstyle"})
            lis = div.findAll("li")
            for li in lis:
                iurl = li.find("a").get("href")
                prev_len = len(url_set)
                url_set.add(iurl)
                if len(url_set) > prev_len:
                    new += 1
                    yield scrapy.Request(iurl, self.parse_item)

            urls = root.find("div", id="pages").findAll("a")
            for u in urls:
                if u.text == "下一页":
                    hasNext = True
                    url = root_domain + u.get("href")
                    print url

    def parse_item(self, response):
        '''
        访问各新闻页面，获取各键值
        :param response:
        :return:
        '''
        self.log('Hi, this is an item page! %s' % response.url)
        item = FenghuoItem()
        root = bs(response.body)

        try:
            item['topPost'] = 1
            item["site_id"] = 17
            item['website_id'] = ''
            item["site_name"] = '襄城区人民政府'
            item["area"] = 958
            item["site_weight"] = 2
            item['countryid'] = 1156
            item['province'] = 1673
            item['city'] = 136
            item["ip"] = socket.gethostbyname("www.xfxc.gov.cn")
            item["site_url"] = "www.xfxc.gov.cn"
            types = root.find("div", attrs={"class": "pagenav"}).findAll("a")
            item["forumurl"] = types[len(types)-1].get("href")
            item["site_type"] = '新闻'
            item["domain_1"] = "xfxc.gov.cn"
            item["domain_2"] = "www"
            item["url"] = response.url
            types = root.find("div", attrs={"class": "pagenav"}).findAll("a")
            item["subname"] = types[len(types)-1].text
            item["pubdate"] = root.find("div", attrs={"class": "info"}).find("span").text
            #替换所有图片标签
            imgs = root.find("div", attrs={"class": "content"}).findAll("img")
            for img in imgs:
                img.replaceWith(img.prettify())
            item["txt"] = root.find("div", attrs={"class": "content"}).text.replace("\r\n", "$*huanhang*$").replace("\n", "$*huanhang*$").replace("\"", "'").replace("<br />", "$*huanhang*$")
            item["txt_len"] = len(item["txt"])
            item["title"] = root.find("h1").text
            item["snatch_time"] = datetime.datetime.now()
            return item
        except:
            #errors are log in error1.json with url
            line = response.url + "\n"
            self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
            self.file.write(line.decode("unicode_escape"))
            pass
