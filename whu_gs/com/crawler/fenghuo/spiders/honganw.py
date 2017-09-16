# -*- coding: UTF-8 -*-

__author__ = 'andy'

'''
Created on 28/7/2015
@author: andy YI
'''

import codecs
import re
import datetime
import socket

import scrapy
from scrapy.contrib.spiders import CrawlSpider
from BeautifulSoup import BeautifulSoup as bs
from fenghuo.items import BaotuoItem
import requests

root_domain = "http://www.redhongan.com"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class HongAnSpider(CrawlSpider):
    name = "haw"
    allowed_domains = ["redhongan.com"]

    start_urls = [
        'http://www.redhongan.com/'
    ]


    def parse(self, response):
        self.log('Hi, this is the first page %s' % response.url)
        root = bs(response.body)
        try:
            names = root.findAll("table")[8].findAll("a")
            xxx = set(['/honganshipin/','http://www.hakjj.com/','http://www.honganbbs.com','http://www.halyzw.com','http://www.hbhakfq.com/'])

            for name in names:
                url1 = name.get("href")
                if url1 in xxx:
                    pass
                elif url1 == 'http://www2.redhongan.com/dangjian/':
                    yield scrapy.Request(url1, self.parse_dangjian)
                else:
                    url = root_domain + url1
                    yield scrapy.Request(url , self.parse_pages)
        except Exception as inst:
            print inst

    def parse_dangjian(self,response):

        self.log('Hi, this is the andy page %s' % response.url)
        root = bs(response.body)
        try:
            url_self = response.url
            url_self = url_self[:url_self.index("/dangjian/")]
            names = root.find("map",attrs={"name":"Map2"}).findAll("area")
            for name in names:
                url1 = name.get("href")
                url = url_self + url1
                #yield scrapy.Request(url1 , self.parse_page)
        except Exception as inst:
            print inst
            pass


        pass

    def parse_pages(self,response):

        self.log('Hi, this is the second page %s' % response.url)
        root = bs(response.body)
        try:
            url_self = response.url
            if url_self == "http://www.redhongan.com/zsyz/":
                names = root.findAll("table")[1].findAll("a")
                for name in names:
                    xxx = name.text
                    if xxx == "":
                        names.remove(name)
            else:
                names = root.findAll("table")[2].findAll("a")
            for name in names:
                url1 = name.get("href")
                subname = name.text
                if url1 in ["http://www.redhongan.com/","http://www.redhongan.com","#"]:
                    pass
                else:
                    url = root_domain + url1
                    yield scrapy.Request(url, self.parse_page,meta={"subname":subname})
        except Exception as inst:
            print inst
            pass


    def parse_page(self,response):
        self.log('Hi, this is the list page %s' % response.url)
        root = bs(response.body)
        url_self = response.url
        try:
            names = root.find("div",attrs={"class":"pages"}).findAll("a")
            l = len(names)
            try:
                name = names[l-2].text
                try:
                  name = name[name.index("...")+3:]
                except:
                  name = name
            except:
                name = 1
                pass
            for i in range(int(name)+1):
                url = url_self + str(i) + ".shtml"
                try:
                   yield scrapy.Request(url, self.parse_items,meta={'subname':response.meta["subname"]})
                except Exception as inst:
                    print inst
                    print "page doesn't exist"
        except Exception as inst:
            print inst
            pass

    def parse_items(self,response):
            self.log('Hi, this is the items page %s' % response.url)
            root = bs(response.body)
            url_self = response.url
            try:
              lables = root.find("table").findNextSiblings()[6].find("td").findAll("tr")[2].findAll("table")[1].find("tr").find("td",attrs={"valign":"top"}).findNextSiblings()[1].find("table").findAll("tr")
            except Exception as inct:
               pass
            try:
                for lable in lables:
                    item = BaotuoItem()
                    url = lable.find("td").findNextSibling().find("a").get("href")
                    item["forumurl"] = url_self
                    item["subname"] = response.meta["subname"]
                    yield scrapy.Request(url, self.parse_item,meta={'item':item})
            except Exception as inct:
               print inct
               pass



    def parse_item(self,response):
        self.log('Hi, this is the item page %s' % response.url)
        root = bs(response.body)


        item = response.meta['item']
        item["url"] = response.url
        item["title"] = root.find("td",attrs={"class":"dabiaoti"}).text
        item["domain_1"] = "redhongan.com"
        item["domain_2"] = "www"
        item["site_id"] = 31
        item["website_id"] = 0
        item["site_name"] ="红安网"
        item["area"] = 3570
        item["countryid"] = 1156
        item["province"] = 1673
        item["city"] = 2508
        item["ip"] = socket.gethostbyname("www.baotuowang.com")
        item["site_url"] = "www.redhongan.com"
        item["site_type"] = "新闻"
        item["snatch_time"] = datetime.datetime.now()
        item["url"] = response.url
        item["pubdate"] = root.find("table").findNextSiblings()[10].find("td").find("tbody").find("tr").findNextSibling().find("tr").findNextSibling().find("tr").findNextSibling().find("font").text
        item["author"] = ""
        try:
            imgs = root.find("div",attrs={"id":"Zoom"}).findAll("img")
            for img in imgs:
                img.replaceWith(img.prettify())
        except:
            pass
        item["txt"] = root.find("div",attrs={"id":"Zoom"}).text.replace("<br />", " ").replace("\r\n", "$*huanhang*$").replace("\"", "‘").replace("","")
        item["txt_len"] = len(item["txt"])


        return item






