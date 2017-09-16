#coding=utf-8
'''
Created on 2015年7月 30日

@author: bohaohan
@说明 ：襄城论坛 爬取         http://www.461700.org/
'''

import codecs
import socket

__author__ = 'bohaohan'

#spider of cntongshan.com
import re
import datetime

__author__ = 'bohaohan'
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from BeautifulSoup import BeautifulSoup as bs
from fenghuo.items import FenghuoItem
import requests

root_domain = "http://www.461700.org/"

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class tongshan_xinxigang_Spider(CrawlSpider):

    name = "xclt"
    start_urls = [
        'http://www.461700.org/index.asp?CurPage=1'
    ]


    # def parse(self, response):
    #     url = "http://www.461700.org/show.asp?id=383&extra=0-3"
    #     yield scrapy.Request(url, self.parse_item)

    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        root_url = response.url

        last_t = "0"
        new = 21
        url = root_url
        has_next = True
        while new > 5 and has_next:
            new = 0
            has_next = False
            r = requests.get(url)
            r.encoding = "gbk"
            root = bs(r.text)
            table = root.find("div", attrs={"id": "wrapper"})
            try:
                trs = table.findAll("tbody")
            except:
                line = response.url + "\n"
                self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
                self.file.write(line.decode("unicode_escape"))
                continue
            for tr in trs:
                item = FenghuoItem()
                item["domain_1"] = "461700.org"
                item["domain_2"] = "www"
                item["site_id"] = 46
                item['website_id'] = ''
                item["site_name"] = '襄城论坛'
                item["area"] = 3507
                item["site_weight"] = 2
                item['countryid'] = 1156
                item['province'] = 1673
                item['city'] = 996
                item["ip"] = socket.gethostbyname("www.461700.org")
                item["site_url"] = "www.461700.org"
                item["forumurl"] = root_url
                item["site_type"] = '论坛'
                item["snatch_time"] = datetime.datetime.now()
                # try:
                item["url"] = root_domain + tr.find("a", attrs={"href": re.compile("^show")}).get("href")
                item["title"] = tr.find("a", attrs={"href": re.compile("^show")}).text
                item["author"] = tr.find("td", attrs={"class": "author"}).find("cite").text
                try:
                    item["reply"] = tr.find("td", attrs={"class": "nums"}).find("strong").text
                except:
                     item["reply"] = ""
                try:
                    item["view"] = tr.find("td", attrs={"class": "nums"}).find("em").text
                except:
                    item["view"] = ""

                try:
                    item["postid"] = tr.findAll("td", attrs={"class": "lastpost"})[1].find("cite").text
                except:
                    item["postid"] = ""

                try:
                    item["subname"] = tr.find("div", attrs={"class": "tietitle"}).find("em").find("a").text
                except:
                    item["subname"] = ""

                new += 1
                print item["url"]
                yield scrapy.Request(item["url"], self.parse_item,  meta={'item': item})

            try:
                urls = root.find("div", attrs={"class": "meneame"}).findAll("a")
                for u in urls:
                    if u.text == "下一页":
                        url = root_domain + u.get("href")
                        has_next = True
                        print url
            except:
                break


    def parse_item(self, response):
        item = response.meta['item']
        #item = FenghuoItem()
        item['articles'] = []
        item["txt"] = ""
        new_root = bs(response.body.decode('gbk'))
        subnames = new_root.find("div", id="nav1").findAll("a")
        item["subname"] = subnames[len(subnames)-1].text
        url = response.url
        hasNext = True
        try:
            while hasNext:
                hasNext = False
                r1 = requests.post(url)
                r1.encoding = 'gbk'
                new_root = bs(r1.text)
                divs = new_root.find("div", id="wrapper").findChildren('table', attrs={"class": "showTie"})
                for div in divs:
                    c_item = FenghuoItem()
                    c_item["topPost"] = 0
                    try:
                        c_item['author'] = div.find("td", attrs={"class": "aa"}).find("a").text
                        c_item['userpage'] = div.find("td", attrs={"class": "aa"}).find("a").text
                        times = div.find("td", attrs={"class": "aa"}).findAll("li")
                        c_item["pubdate"] = times[len(times)-1].text
                        item["updatetime"] = c_item["pubdate"]
                        try:
                            c = div.find("td", attrs={"class": "bb"}).find("span").text
                            c_item["postfloor"] = c[:c.index("阅")-1]
                            if c_item["postfloor"] == "楼主":
                                c_item["postfloor"] = 1
                                c_item["topPost"] = 1
                                item["pubdate"] = c_item["pubdate"]
                                item['userpage'] = c_item['userpage']
                        except:
                            c = div.find("td", attrs={"class": "bb"}).find("div", attrs={"class": "tiefoot s_clear"}).find("span").text
                            c = c[c.index("回复")+2:]
                            c_item["postfloor"] = c[:c.index("楼")]
                            c_item["postfloor"] = int(c_item["postfloor"]) + 1
                        styles = div.findAll("style")
                        scripts = div.findAll("script")
                        for style in styles:
                            style.clear()
                        for script in scripts:
                            script.clear()

                        #替换所有图片标签
                        imgs = div.find("td", attrs={"class": "bb"}).find("div").findAll("img")
                        for img in imgs:
                            img.replaceWith(img.prettify())
                        c_item["txt"] = div.find("td", attrs={"class": "bb"}).find("div").text.replace("<br />", " ").replace("\r\n", "$*huanhang*$").replace("\"", "‘")
                        strs = str(c_item["postfloor"]) + "." + str(c_item["txt"]) + "\n"
                        item["txt"] += strs
                        item["txt_len"] = len(item["txt"])
                        c_item["txt_len"] = len(c_item["txt"])
                        item['articles'].append(dict(c_item))

                    except:
                        line = str(div) + "\n"
                        self.file = codecs.open('error2.json', 'ab', encoding='utf-8')
                        self.file.write(line.decode("unicode_escape"))
                        pass
                    #
                    # # #clear css, js , advertisement and messy code
                try:
                    curls = new_root.find("div", attrs={"class": "meneame"}).findAll("a")
                    for curl in curls:
                        if curl.text == "下一页" and url != root_domain + curl.get("href"):
                            url = curl
                            hasNext = True
                            print url
                except:
                    pass
            return item
        except:
            line = response.url + "\n"
            self.file = codecs.open('error2.json', 'ab', encoding='utf-8')
            self.file.write(line.decode("unicode_escape"))
            pass



