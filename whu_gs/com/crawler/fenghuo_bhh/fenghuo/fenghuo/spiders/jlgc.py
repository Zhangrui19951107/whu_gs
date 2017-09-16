# -*- coding: UTF-8 -*-

#spider of cntongshan.com
'''
Created on 2015年7月18日

@author: bohaohan
@introduction: spider of cntongshan.com
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

root_domain = "http://www.cntongshan.com"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TongShanChinaSpider(CrawlSpider):
    name = "cnts"
    allowed_domains = ["cntongshan.com"]

    start_urls = [
        'http://www.cntongshan.com/News/'
    ]

    def parse(self, response):
        '''

        :param response:
        :return:

        取各版块的url并传入到parse_pages

        '''
        #test
        # url = 'http://www.cntongshan.com/News/NewsShow-1322.html'
        # yield scrapy.Request(url, self.parse_item,  meta={'forumurl': '123'})
        #end test

        self.log('Hi, this is an item page! %s' % response.url)
        root = bs(response.body)

        #use navigation
        curls = []
        divs = root.findAll("div", attrs={"class": "title"})
        for div in divs:
            try:
                url = div.find("span").find("a", attrs={"href": re.compile("^NewsList")})
                curls.append(url.get("href"))
            except:
                pass

        for url in curls:
            yield scrapy.Request(root_domain + "/News/" + url, self.parse_pages)

    def parse_pages(self, response):
        '''
        获取每个版块的页数，并生成各页面的url传入parse_page
        利用meta传值，获取版块url
        :param response:
        :return:
        '''
        self.log('Hi, this is an item page! %s' % response.url)
        root = bs(response.body)
        pageText = root.find("div", attrs={"class": "AntPage"}).find("li").text
        pageText = pageText[pageText.index("/")+1:pageText.index(" ")]
        root_url = response.url
        root_url = root_url[:root_url.index(".html")]
        for i in range(1, int(pageText)+1):
            url = root_url + "-AA-p" + str(i) +".html"
            yield scrapy.Request(url, self.parse_page,  meta={'forumurl': root_url + "-AA-p1.html"})

    def parse_page(self, response):
        '''
        获取各页面的新闻链接并调用parse_item
        :param response:
        :return:
        '''
        self.log('Hi, this is an list page! %s' % response.url)
        root = bs(response.body)
        uls = root.findAll("ul", attrs={"class": "l_l"})
        forumurl = response.meta['forumurl']
        for ul in uls:
            urls = ul.findAll("a", attrs={"href": re.compile("^http://www.cntongshan.com")})
            for url in urls:
                yield scrapy.Request(url.get("href"), self.parse_item,  meta={'forumurl': forumurl})

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
            item["site_name"] = '中国通山网'
            item["area"] = 958
            item["site_weight"] = 2
            item['countryid'] = 1156
            item['province'] = 1673
            item['city'] = 136
            item["ip"] = socket.gethostbyname("www.cntongshan.com")
            item["site_url"] = "www.cntongshan.com"
            item["forumurl"] = response.meta['forumurl']
            item["site_type"] = '新闻'
            item["url"] = response.url
            url = response.url
            id = url[url.index("-")+1:]
            id = id[:id.index(".")]
            item["parent_type"] = root.find("a", attrs={"class": "Current"}).text
            item["subname"] = root.find("a", attrs={"class": "A", "target": "_blank"}).text
            str = root.find("div", attrs={"class": "Title_h1"}).find("div").text
            str1 = str[str.index('20'):]
            item["pubdate"] = str1[:str1.index('\n')-2]
            try:
                str2 = str[str.index('作者')+2:]
                item["author"] = str2[:str2.index("浏览")].replace("\r\n", "$*huanhang*$")
            except:
                item["author"] = ""

            #because view is get by ajax through GET, so we should use requests to get view
            #id is the id of the news , getted by url
            r = requests.get("http://www.cntongshan.com/public/ajax.aspx?action=addnum&id=" + id + "&t=4&_=1437061503826")
            item["view"] = int(r.text[:r.text.index(",")])

            #替换所有图片标签
            imgs = root.find("div", attrs={"class": "content_main"}).findAll("img")
            for img in imgs:
                img.replaceWith(img.prettify())

            #website_name
            try:
                website_name = root.find("div", attrs={"class": "content_main"}).find("div", attrs={"class": "content_author"}).text
                website_name = website_name[website_name.index('本文来源')+5:]
                website_name = website_name[:website_name.index('\n')-1]
                item['website_name'] = website_name
            except:
                item['website_name'] = ''
            item["txt"] = root.find("div", attrs={"class": "content_main"}).text.replace("\r\n", "$*huanhang*$").replace("\n", "$*huanhang*$").replace("\"", "'").replace("<br />", "$*huanhang*$")
            item["txt_len"] = len(item["txt"])
            item["title"] = root.find("h1").text
            item["domain_1"] = "cntongshan.com"
            item["domain_2"] = "www"
            item["snatch_time"] = datetime.datetime.now()
            return item
        except:
            #errors are log in error1.json with url
            line = response.url + "\n"
            self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
            self.file.write(line.decode("unicode_escape"))
            pass
