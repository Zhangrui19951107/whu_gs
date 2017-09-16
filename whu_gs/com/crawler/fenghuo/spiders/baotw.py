# -*- coding: utf-8 -*-
import re
import datetime

__author__ = 'andy'


import scrapy
import codecs
import socket
import codecs , json
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from BeautifulSoup import BeautifulSoup as bs
from fenghuo.items import BaotuoItem
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class baotw_Spider(CrawlSpider):
    name="baotw"
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
        for i in range(1,int(totalpage)+1):
            url = root_url + pageid + "&page=" + str(i)
            yield  scrapy.Request(url,self.parse_page,meta={'forumurl':forumurl,'pageid':pageid})

    def parse_page(self,response):

        self.log('Hi, this is the third page %s' % response.url)
        root = bs(response.body)
        forumurl = response.url
        pageid = response.meta['pageid']
        if pageid == '130':
             a_tbody = root.find("div",attrs={"id":"threadlist"}).find("div",attrs={"class":"eis_sortsublist"}).findAll("tbody")
             for bbb in a_tbody:
              try:
                url = bbb.find("th").find("a",attrs={"href":re.compile(".*thread-\d{5}.+")}).get("href")
                try:
                   time1 = bbb.findAll("td",attrs={"class":"by"})[1].find("em").find("a")
                   try:
                        updatetime = time1.find("span").get("title")
                   except:
                        updatetime = time1.text
                except:
                    updatetime = ""
                url = url[url.index("thread"):url.index(".html")+5]
                url = "http://www.baotuowang.com/" + url
                yield scrapy.Request(url,callback=self.parse_item,meta={'updatetime':updatetime,'forumurl':response.meta['forumurl']})
              except Exception as inst:
                 print inst
                 pass
        elif pageid == '244':
             a_tbody = root.find("ul",attrs={"id":"waterfall"}).findAll("li")
             for bbb in a_tbody:
                 url = bbb.find("div",attrs={"class":"c cl"}).find("a").get("href")
                 updatetime = ""
                 url = url[url.index("thread"):]
                 url = "http://www.baotuowang.com/" + url
                 yield scrapy.Request(url,callback=self.parse_item,meta={'updatetime':updatetime,'forumurl':response.meta['forumurl']})
        else:
            a_tbody = root.find("table",attrs={"id":"threadlisttableid"}).findAll("tbody",attrs={"id":re.compile(".+thread.+")})
            for bbb in a_tbody:
             try:
                url = bbb.find("th").find("a",attrs={"href":re.compile(".*thread-\d{2}.+")}).get("href")
                try:
                   time1 = bbb.findAll("td",attrs={"class":"by"})[1].find("em").find("a")
                   try:
                        updatetime = time1.find("span").get("title")
                   except:
                        updatetime = time1.text
                except:
                    updatetime = ""
                    url = url[url.index("thread"):url.index(".html")+5]
                url = "http://www.baotuowang.com/" + url
                yield scrapy.Request(url,callback=self.parse_item,meta={'updatetime':updatetime,'forumurl':response.meta['forumurl']})
             except Exception as inst:
                  print inst
                  pass




    def parse_item(self,response):
        self.log('Hi, this is an item page! %s' % response.url)
        item = BaotuoItem()
        root = bs(response.body)

        item["domain_1"] = "baotuowang.com"
        item["domain_2"] = "www"
        item["site_id"] = 14
        item["website_id"] = ""
        item["site_name"] = "包砣网"
        item["area"] = 958
        item["countryid"] = 2
        item["province"] = 1673
        item["city"] = 136
        item["ip"] = socket.gethostbyname("www.baotuowang.com")
        item["site_url"] = "www.baotuowang.com"
        item["site_type"] = "论坛"
        item["snatch_time"] = datetime.datetime.now()
        item["url"] = response.url
        try:
            item["forumurl"] = response.meta["forumurl"]
            t = root.find("title").text
            item["title"] = t[:t.index(" -")]
            item["author"] =  root.find("div",attrs={"id":"postlist"}).find("div",attrs={"class":"pls favatar"}).find("div",attrs={"class":"authi"}).find("font").text
            item["userpage"] = "www.baotuowang.com/"+ root.find("div",attrs={"id":"postlist"}).find("div",attrs={"class":"pls favatar"}).find("div",attrs={"class":"authi"}).find("a").get("href")
            url_id = root.find("div",attrs={"id":"postlist"}).find("div",attrs={"class":"pls favatar"}).find("div",attrs={"class":"authi"}).find("a").get("href")
            url_id = url_id[url_id.index("uid=")+4:]
            item["userid"] = url_id

            item["reply"] = root.find("div",attrs={"class":"hm ptn"}).findAll("span",attrs={"class":"xi1"})[1].text
            item["view"] = root.find("div",attrs={"class":"hm ptn"}).findAll("span",attrs={"class":"xi1"})[0].text
            item["postid"] = "can't get"
            t = t[t.index(" - ")+3:]
            item["subname"] = t[:t.index(" - ")]
            item["updatetime"] = response.meta["updatetime"]
        except:
            line = str(root)+"\n"
            self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
            self.file.write(line.decode("unicode_escape"))

        try:
            item["articles"] =[]
            new_root = bs(response.body.decode('gbk'))
            try:
               pageText = new_root.find("div", attrs={"id": "pgt"}).find("div", attrs={"class": "pgt"}).find("div",attrs={"class":"pg"}).find("span").text
               pageText = pageText[pageText.index("/")+2:]
               pageText = pageText[:pageText.index(" ")]
            except Exception as inct:
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
        except Exception as inst:
            print inst
            pass





























