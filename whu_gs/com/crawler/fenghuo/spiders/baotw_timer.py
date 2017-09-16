# -*- coding: utf-8 -*-

import re
import datetime

__author__ = 'andy'


import scrapy
import codecs
import socket
import datetime
import codecs , json
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from BeautifulSoup import BeautifulSoup as bs
from fenghuo.items import BaotuoItem

import requests

root_domain = "http://www.baotuowang.com/"

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class baotw_Spider(CrawlSpider):
    name="baotw_timer"
    allowed_domains = ["baotuowang.com"]
    root_domain = "www.baotuowang.com"
    start_urls = ['http://www.baotuowang.com/forum.php']

    #global hrefs

    hrefs = set([])

    def parse(self,response):
        self.log('Hi, this is the first page %s' % response.url)
        root = bs(response.body)

        names = root.findAll("div", attrs={"class":"bm bmw  flg cl"})

        for name in names:
            subnames = name.find("div",attrs={"class":"bm_c"}).findAll("td",attrs={"class":"fl_g"})
            for subname in subnames:
                url1 = subname.find("a").get("href")
                url2 = response.url
                url2 = url2[:url2.index("forum.php")]
                url1 = url2 + url1
                print url1
                yield scrapy.Request(url1 , self.parse_pages)

    def parse_pages(self,response):
        self.log('Hi, this is the second page %s' % response.url)
        root = bs(response.body)
        forumurl = response.url
        pageid = forumurl[forumurl.index("orum-")+5:forumurl.index("-1.html")]
        print forumurl
        try:
            pageText = root.find("div", attrs={"class": "pg"}).find("span").text
            pageText = pageText[pageText.index("/")+2:]
            totalpage = pageText[:pageText.index(" ")]
        except:
            totalpage = 1
        root_url = "http://www.baotuowang.com/forum.php?mod=forumdisplay&fid="

        new = 33
        hasNext = True
        url = root_url + pageid + "&page=" + str(1)
        while new > 32 and hasNext:
            r = requests.get(url)
            root = bs(r.text)
            try:
                url = root.find("div", attrs={"class": "pg"}).find("a", attrs={"class": "nxt"}).get("href")
            except:
                hasNext = False

            table = root.find("div", id="threadlist")
            trs = table.findAll("tr")
            for tr in trs:
                item = BaotuoItem()
                item["domain_1"] = "baotuowang.com"
                item["domain_2"] = "www"
                item["site_id"] = 14
                item['website_id'] = ''
                item["site_name"] = '包砣网'
                item["area"] = 958
                item["site_weight"] = 2
                item['countryid'] = 1156
                item['province'] = 1673
                item['city'] = 136
                item["ip"] = socket.gethostbyname("www.baotuowang.com")
                item["site_url"] = "www.baotuowang.com"
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
                        new += 1
                        yield scrapy.Request(item["url"], self.parse_item,  meta={'item': item})

                    if item["updatetime"] and item["updatetime"] == last_t:
                        new += 1
                        #update before
                        pass

                except Exception as e:
                    #print e
                    #print tr
                    line = str(tr) + "\n"
                    self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
                    self.file.write(line.decode("unicode_escape"))

    def parse_page(self, response):
        self.log('Hi, this is an list page! %s' % response.url)
        root = bs(response.body.decode('gbk'))
        table = root.find("div", id="threadlist")
        trs = table.findAll("tr")
        for tr in trs:
            item = BaotuoItem()
            item["domain_1"] = "baotuowang.com"
            item["domain_2"] = "www"
            item["site_id"] = 14
            item['website_id'] = ''
            item["site_name"] = '包砣网'
            item["area"] = 958
            item["site_weight"] = 2
            item['countryid'] = 1156
            item['province'] = 1673
            item['city'] = 136
            item["ip"] = socket.gethostbyname("www.baotuowang.com")
            item["site_url"] = "www.baotuowang.com"
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
             pageText = new_root.find("div", attrs={"id": "pgt"}).find("div", attrs={"class": "pgt"}).find("div",attrs={"class":"pg"}).find("span").text
             pageText = pageText[pageText.index("/")+2:]
             pageText = pageText[:pageText.index(" ")]
        except:
            pageText = 1
        url = response.url
        try:
            for page in range(1,int(pageText)+1):
                    try:
                      r1 = requests.post(url)
                    except:
                      new_root = bs(r1.text)
                    try:
                       divs = new_root.findChildren('div', attrs={"id": re.compile("^post_[0-9]")})
                    except Exception as inct:
                        print inct
                    for div in divs:
                       c_item = BaotuoItem()
                       c_item["topPost"] = 0
                       c_item['author'] = div.find("table").find("td", attrs={"class": "pls"}).find("div", attrs={"class": "authi"}).find("a").text
                       c_item['userpage'] = div.find("table").find("td", attrs={"class": "pls"}).find("div", attrs={"class": "authi"}).find("a").get("href")
                       try:
                           pubdate = div.find("table").find("td", attrs={"class": "plc"}).find("div", attrs={"class": "authi"}).find("em").text
                           c_item["pubdate"] = pubdate[pubdate.index("发表于 ")+4:]
                       except Exception as inct:
                           print "format is wrong"
                       try:
                             c_item["postfloor"] = div.find("table").find("td", attrs={"class": "plc"}).findNextSibling().find("div", attrs={"class": "pi"}).find("strong").find("em").text
                       except Exception as inct:
                            try:
                              c_item["postfloor"] = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("div", attrs={"class": "pi"}).find("strong").find("em").text
                            except:
                                try:
                                  name = div.find("table").find("td", attrs={"class": "plc"}).find("div", attrs={"class": "pi"}).find("strong").find("a").text
                                  if "楼主" in name:
                                      c_item["postfloor"] = 1
                                  elif "沙发" in name:
                                      c_item["postfloor"] = 2
                                  elif "板凳" in name:
                                      c_item["postfloor"] = 3
                                  elif "地板" in name:
                                      c_item["postfloor"] = 4
                                  else:
                                      c_item["postfloor"] = 123

                                  if c_item["postfloor"] == 1:
                                      c_item["topPost"] = 1
                                except:
                                    try:
                                      name = div.find("table").find("td", attrs={"class": "plc"}).find("div", attrs={"class": "pi"}).find("strong").find("a").text
                                      if "楼主" in name:
                                          c_item["postfloor"] = 1
                                      elif "沙发" in name:
                                          c_item["poschaxuntfloor"] = 2
                                      elif "板凳" in name:
                                          c_item["postfloor"] = 3
                                      elif "地板" in name:
                                          c_item["postfloor"] = 4
                                      else:
                                          c_item["postfloor"] = 123

                                      if c_item["postfloor"] == 1:
                                          c_item["topPost"] = 1
                                    except Exception as inct:
                                        print inct
                           # s = len(divs)
                       styles = div.findAll("style")
                       scripts = div.findAll("script")
                       for style in styles:
                           style.clear()
                       for script in scripts:
                           script.clear()
                       apts = new_root.findAll("tr",attrs={"class":"ad"})
                       for apt in apts:
                           apt.clear()
                       advs = div.findAll("div", attrs={"class": "a_pt"})
                       for adv in advs:
                           adv.clear()
                       m_codes = new_root.findAll("span", attrs={"style": "display:none"})
                       for m_code in m_codes:
                           m_code.clear()
                       try:
                           imgs = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("table").findAll("img")
                           for img in imgs:
                                img.replaceWith(img.prettify())

                           c_item["txt"] = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("table").text.replace("<br />", " ").replace("\r\n", "$*huanhang*$").replace("\"", "‘")
                           c_item["txt_len"] = len(c_item["txt"])
                           item['articles'].append(dict(c_item))
                       except Exception as inst:
                           pass

                    try:
                      url1 = new_root.find("div",attrs={"class":"pgbtn"}).find("a").get("href")
                      url = "http://www.baotuowang.com/" + url1
                    except Exception as inst:
                        pass
        except Exception as inst:
            line = response.url + "\n"
            self.file = codecs.open('error2.json', 'ab', encoding='utf-8')
            self.file.write(line.decode("unicode_escape"))
            pass
        return item







