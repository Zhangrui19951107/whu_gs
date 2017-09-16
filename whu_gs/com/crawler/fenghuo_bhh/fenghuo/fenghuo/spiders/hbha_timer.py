#coding=utf-8
'''
Created on 2015年7月 29日

@author: bohaohan
@说明 ：通山论坛 爬取         http://bbs.hbha.com.cn/
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

root_domain = "http://bbs.hbha.com.cn/"

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class tongshan_xinxigang_Spider(CrawlSpider):

    name = "hbhat"
    start_urls = [
        'http://bbs.hbha.com.cn/forum.php'
        # 'http://bbs.hbha.com.cn/forum.php?mod=forumdisplay&fid=102'
        # 'http://bbs.hbha.com.cn/forum.php?mod=viewthread&tid=89471#lastpost'
    ]


    def parse(self, response):

        self.log('Hi, this is an item page! %s' % response.url)
        root = bs(response.body.decode('gbk'))
        #use sections
        url_s = set([])

        #test
        # url = "http://www.437600.net/thread-5727-1-1.html"
        # yield scrapy.Request(url, self.parse_item)
        #end test

        urls = root.findAll("a", attrs={"href": re.compile("^forum\.php\?mod=forumdisplay")})
        for url in urls:
            curl = root_domain + url.get("href")
            url_s.add(curl)
        i = 0
        for url in url_s:
            yield scrapy.Request(url, self.parse_pages)


    def parse_pages(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        root_url = response.url

        last_t = "0"
        new = 21
        url = root_url
        while new > 20:
            new = 0
            r = requests.get(url)
            r.encoding = "gbk"
            root = bs(r.text)

            table = root.find("table", id="threadlisttableid")
            # print table
            try:
                trs = table.findAll("tr")
            except:
                line = response.url + "\n"
                self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
                self.file.write(line.decode("unicode_escape"))
                continue
            for tr in trs:
                item = FenghuoItem()
                item["domain_1"] = "hbha.com.cn"
                item["domain_2"] = "bbs"
                item["site_id"] = 36
                item['website_id'] = ''
                item["site_name"] = '红安论坛'
                item["area"] = 3507
                item["site_weight"] = 2
                item['countryid'] = 1156
                item['province'] = 1673
                item['city'] = 2508
                item["ip"] = socket.gethostbyname("bbs.hbha.com.cn")
                item["site_url"] = "bbs.hbha.com.cn"
                item["forumurl"] = root_url
                item["site_type"] = '论坛'
                item["snatch_time"] = datetime.datetime.now()
                try:
                    item["url"] = root_domain + tr.find("a", attrs={"href": re.compile("^forum")}).get("href")
                    item["title"] = tr.find("th").find("a", attrs={"href": re.compile("^forum")}).text
                    item["author"] = tr.find("td", attrs={"class": "by"}).find("cite").find("a").text
                    item["userpage"] = root_domain + tr.find("td", attrs={"class": "by"}).find("cite").find("a").get("href")
                    url_id = tr.findAll("td", attrs={"class": "by"})[0].find("cite").find("a").get("href")
                    url_id = url_id[url_id.index("uid=")+4:]
                    item["userid"] = url_id
                    try:
                        item["reply"] = tr.find("td", attrs={"class": "num"}).find("a").text
                    except:
                         item["reply"] = ""
                    try:
                        item["view"] = tr.find("td", attrs={"class": "num"}).find("em").text
                    except:
                        item["view"] = ""

                    try:
                        item["postid"] = tr.findAll("td", attrs={"class": "by"})[1].find("cite").find("a").text
                    except:
                        item["postid"] = ""

                    try:
                        item["subname"] = root_domain + tr.find("th").find("em").find("a").text
                    except:
                        item["subname"] = ""

                    try:
                        time1 = tr.findAll("td", attrs={"class": "by"})[1].find("em").find("a")
                        try:
                            item["updatetime"] = time1.find("span").get("title")
                        except:
                            item["updatetime"] = time1.text

                    except:
                        item["updatetime"] = ""
                    #explore the content of the page

                    #增量的判断
                    if item["updatetime"] and item["updatetime"] > last_t:
                        new += 1
                        print item["url"]
                        yield scrapy.Request(item["url"], self.parse_item,  meta={'item': item})

                    if item["updatetime"] and item["updatetime"] == last_t:
                        new += 1
                        #update before


                except Exception as e:
                    line = str(tr) + "\n"
                    self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
                    self.file.write(line.decode("unicode_escape"))
            try:
                url = root_domain + root.find("div", attrs={"class": "pg"}).find("a", attrs={"class": "nxt"}).get("href")
                print url
            except:
                break



    def parse_page(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        root = bs(response.body.decode('gbk'))
        table = root.find("div", id="threadlist")
        trs = table.findAll("tr")
        for tr in trs:
            item = FenghuoItem()
            item["domain_1"] = "hbha.com.cn"
            item["domain_2"] = "bbs"
            item["site_id"] = 36
            item['website_id'] = ''
            item["site_name"] = '红安论坛'
            item["area"] = 3507
            item["site_weight"] = 2
            item['countryid'] = 1156
            item['province'] = 1673
            item['city'] = 2508
            item["ip"] = socket.gethostbyname("bbs.hbha.com.cn")
            item["site_url"] = "bbs.hbha.com.cn"
            item["forumurl"] = response.meta['forumurl']
            item["site_type"] = '论坛'
            item["snatch_time"] = datetime.datetime.now()
            try:
                item["url"] = root_domain + tr.find("a", attrs={"href": re.compile("^thread")}).get("href")
                item["title"] = tr.find("th").find("a", attrs={"href": re.compile("^thread")}).text
                item["author"] = tr.find("td", attrs={"class": "by"}).find("cite").find("a").text
                item["userpage"] = root_domain + tr.find("td", attrs={"class": "by"}).find("cite").find("a").get("href")
                url_id = tr.findAll("td", attrs={"class": "by"})[0].find("cite").find("a").get("href")
                url_id = url_id[url_id.index("uid-")+4:]
                item["userid"] = url_id[:url_id.index(".html")]
                try:
                    item["reply"] = tr.find("td", attrs={"class": "num"}).find("a").text
                except:
                     item["reply"] = ""
                try:
                    item["view"] = tr.find("td", attrs={"class": "num"}).find("em").text
                except:
                    item["view"] = ""

                try:
                    item["postid"] = tr.findAll("td", attrs={"class": "by"})[1].find("cite").find("a").text
                except:
                    item["postid"] = ""

                try:
                    item["subname"] = root_domain + tr.find("th").find("em").find("a").text
                except:
                    item["subname"] = ""

                try:
                    time1 = tr.findAll("td", attrs={"class": "by"})[1].find("em").find("a")
                    try:
                        item["updatetime"] = time1.find("span").get("title")
                    except:
                        item["updatetime"] = time1.text

                except:
                    item["updatetime"] = ""
                #explore the content of the page

                #增量的判断
                last_t = ""
                if item["updatetime"] and item["updatetime"] > last_t:
                    yield scrapy.Request(item["url"], self.parse_item,  meta={'item': item})

                if item["updatetime"] and item["updatetime"] == last_t:
                    #update before
                    pass

            except Exception as e:
                #print e
                #print tr
                line = str(tr) + "\n"
                self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
                self.file.write(line.decode("unicode_escape"))

    def parse_item(self, response):
        item = response.meta['item']
        item['articles'] = []
        new_root = bs(response.body.decode('gbk'))
        subnames = new_root.find("div", id="pt").findAll("a")
        item["subname"] = subnames[len(subnames)-2].text
        try:
            pageText = new_root.find("div", attrs={"class": "pg"}).find("span").text

            pageText = pageText[pageText.index("/")+2:]
            pageText = pageText[:pageText.index(" ")]
        except:
            pageText = 1
        url = response.url
        hasNext = True
        try:
            while hasNext:
                hasNext = False
                r1 = requests.post(url)
                r1.encoding = 'gbk'
                new_root = bs(r1.text)
                divs = new_root.findChildren('div', attrs={"id": re.compile("^post_[0-9]")})
                for div in divs:
                    c_item = FenghuoItem()
                    c_item["topPost"] = 0
                    c_item['author'] = div.find("table").find("td", attrs={"class": "pls"}).find("div", attrs={"class": "authi"}).find("a").text

                    c_item['userpage'] = div.find("table").find("td", attrs={"class": "pls"}).find("div", attrs={"class": "authi"}).find("a").get("href")

                    #获取四种pubdate结构的方式
                    try:
                        c_item["pubdate"] = div.find("table").find("td", attrs={"class": "plc"}).find("div", attrs={"class": "authi"}).find("em").find("span").get("title")

                    except:
                        try:
                            t_time = div.find("table").find("td", attrs={"class": "plc"}).find("div", attrs={"class": "authi"}).find("em").text
                            c_item["pubdate"] = t_time[t_time.index(" ")+1:]

                        except:
                            try:
                                c_item["pubdate"] = div.find("table").find("td", attrs={"class": "plc comiis_vtx"}).find("div", attrs={"class": "authi"}).find("em").find("span").get("title")

                            except:
                                try:
                                    t_time = div.find("table").find("td", attrs={"class": "plc comiis_vtx"}).find("div", attrs={"class": "authi"}).find("em").text
                                    c_item["pubdate"] = t_time[t_time.index(" ")+1:]
                                except:
                                    raise
                    try:
                        c_item["postfloor"] = div.find("table").find("td", attrs={"class": "plc"}).find("div", attrs={"class": "pi"}).find("em").text
                        if int(c_item["postfloor"]) == 1:
                            c_item["topPost"] = 1
                    except:
                        try:
                            c_item["postfloor"] = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("strong").find("em").text
                            if int(c_item["postfloor"]) == 1:
                                c_item["topPost"] = 1
                        except:
                            c_item["postfloor"] = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("strong").text
                            if c_item["postfloor"] == "楼主":
                                c_item["postfloor"] = 1
                                c_item["topPost"] = 1


                    # #clear css, js , advertisement and messy code
                    styles = div.findAll("style")
                    scripts = div.findAll("script")
                    for style in styles:
                        style.clear()
                    for script in scripts:
                        script.clear()
                    advs = div.findAll("div", attrs={"class": "attach_nopermission attach_tips"})
                    for adv in advs:
                        adv.clear()
                    m_codes = new_root.findAll("span", attrs={"style": "display:none"})
                    for m_code in m_codes:
                        m_code.clear()
                    m_codes = new_root.findAll("font", attrs={"class": "jammer"})
                    for m_code in m_codes:
                        m_code.clear()

                    #替换所有图片标签
                    imgs = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("table").findAll("img")
                    for img in imgs:
                        img.replaceWith(img.prettify())

                    c_item["txt"] = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("table").text.replace("<br />", " ").replace("\r\n", "$*huanhang*$").replace("\"", "‘")
                    c_item["txt_len"] = len(c_item["txt"])
                    item['articles'].append(dict(c_item))

                try:
                    url = root_domain + new_root.find("div", attrs={"class": "pgbtn"}).find("a").get("href")
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



