# -*- coding: utf-8 -*-

__author__ = 'andy'



import  re
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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
VISITEDLINK = {'thread-71899-1-1.html':0,'thread-26763-1-1.html':0,'thread-70580-1-1.html':0,'thread-1222-1-1.html':0,'thread-70581-1-1.html':0}

class hsbbs_Spider(CrawlSpider):
    name="hsbbs"
    allowed_domains = ["honganbbs.com"]
    root_domain = "www.honganbbs.com"
    start_urls = ['http://www.honganbbs.com/forum.php']


    def parse(self, response):
        self.log('Hi, this is the first page %s' % response.url)

        root = bs(response.body)
        names = root.findAll("div", attrs={"class":"bm bmw  flg cl"})
        for name in names:
            subnames = name.find("div",attrs={"class":"bm_c"}).findAll("td",attrs={"class":"fl_g"})
            for subname in subnames:
                url1 = subname.find("dt").find("a").get("href")
                url2 = response.url
                url2 = url2[:url2.index("forum.php")]
                url1 = url2 + url1
                yield scrapy.Request(url1 , self.parse_pages)

    def parse_pages(self,response):
        self.log('Hi, this is the second page %s' % response.url)
        root = bs(response.body)
        item = BaotuoItem()
        forumurl = response.url
        pageid = forumurl[forumurl.index("orum-")+5:forumurl.index("-1.html")]
        try:
            pageText = root.find("div", attrs={"class": "pg"}).find("span").text
            pageText = pageText[pageText.index("/")+2:]
            totalpage = pageText[:pageText.index(" ")]
        except:
            totalpage = 1
        root_url = "http://www.honganbbs.com/forum-" + pageid
        for i in range(0,int(totalpage)+1):
            url = root_url + "-" + str(i)+".html"
            yield  scrapy.Request(url,self.parse_page,meta={'forumurl':forumurl})


    def parse_page(self,response):
            self.log('Hi, this is the third page %s' % response.url)
            root = bs(response.body)
            global VISITEDLINK
            a_tbody = root.find("div",attrs={"id":"threadlist"}).findAll("tbody",attrs={"id":re.compile(".+thread.+")})
            for bbb in a_tbody:
                 icn_url = bbb.find("td",attrs={"class":"icn"}).find("a").get("href")
                 icn_url = str(icn_url)
                 if icn_url in VISITEDLINK:
                     flag = VISITEDLINK.get(icn_url)
                     if flag == 1:
                         continue
                     elif flag == 0:
                         VISITEDLINK[icn_url] = 1
                         pass
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
                    user_id=bbb.find("td",attrs={"class":"by"}).find("a").get("href")
                    user_id = user_id[user_id.index("-uid-")+5:user_id.index(".html")]
                    url = "http://www.honganbbs.com/" + url
                    yield scrapy.Request(url,callback=self.parse_item,meta={'updatetime':updatetime,'forumurl':response.meta['forumurl']})
                 except Exception as inst:
                      print inst
                      pass


    def parse_item(self,response):
        self.log('Hi, this is an item page! %s' % response.url)
        item = BaotuoItem()
        root = bs(response.body)

        item["domain_1"] = "honganbbs.com"
        item["domain_2"] = "www"
        item["site_id"] = 3570
        item["website_id"] = ""
        item["site_name"] = "红安论坛"
        item["area"] = 958
        item["countryid"] = 1156
        item["province"] = 1673
        item["city"] = 2508
        item["ip"] = socket.gethostbyname("www.honganbbs.com")
        item["site_url"] = "www.honganbbs.com"
        item["site_type"] = "论坛"
        item["snatch_time"] = datetime.datetime.now()
        item["url"] = response.url
        try:
            item["forumurl"] = response.meta["forumurl"]
            t = root.find("title").text
            item["title"] = t[:t.index(" -")]
            item["author"] =  root.find("div",attrs={"id":"postlist"}).find("div",attrs={"id":re.compile(".*post_[0-9].+")}).find("div",attrs={"class":"authi"}).find("a").text
            item["userpage"] =root.find("div",attrs={"id":"postlist"}).find("div",attrs={"id":re.compile(".*post_[0-9].+")}).find("div",attrs={"class":"authi"}).find("a").get("href")
            url_id = item["userpage"]
            url_id = url_id[url_id.index("uid-")+4:url_id.index(".html")]
            item["userid"] = url_id
            item["reply"] = root.find("div",attrs={"class":"eis_pl_tc"}).findAll("span",attrs={"class":"xi1"})[1].text
            item["view"] = root.find("div",attrs={"class":"eis_pl_tc"}).findAll("span",attrs={"class":"xi1"})[0].text
            item["postid"] = "can't get"
        except Exception as inst:
            print inst
            line = str(root)+"\n"
            self.file = codecs.open('error1.json', 'ab', encoding='utf-8')
            self.file.write(line.decode("unicode_escape"))

        try:
            item['articles']=""
            new_root = bs(response.body.decode('gbk'))
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
                    except Exception as inst:
                      print inst
                      new_root = bs(r1.text)
                    try:
                       divs = new_root.findAll('div', attrs={"id": re.compile("^post_[0-9].+")})

                    except Exception as inct:
                        print inct
                    for div in divs:
                       c_item = BaotuoItem()
                       c_item["topPost"] = 0
                       c_item['author'] = div.find("table").find("td", attrs={"class": "pls"}).find("div", attrs={"class": "authi"}).find("a").text
                       c_item['userpage'] = div.find("table").find("td", attrs={"class": "pls"}).find("div", attrs={"class": "authi"}).find("a").get("href")
                       try:
                           pubdate = div.find("td",attrs={"class": "plc"}).find("div", attrs={"class": "authi"}).find("em").text
                           c_item["pubdate"] = pubdate[pubdate.index("发表于 ")+4:]
                       except Exception as inct:
                           print inct
                           print "format is wrong"
                       try:
                             c_item["postfloor"] = div.find("td", attrs={"class": "plc"}).findNextSibling().find("div", attrs={"class": "pi"}).find("strong").find("em").text
                       except Exception as inct:
                            try:
                              c_item["postfloor"] = div.find("table").find("td", attrs={"class": "pls"}).findNextSibling().find("div", attrs={"class": "pi"}).find("strong").find("em").text
                            except:
                                try:
                                  name = div.find("td", attrs={"class": "plc"}).find("div", attrs={"class": "pi"}).find("strong").find("a").text
                                  print name
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
                                      name = div.find("table").find("td", attrs={"class": "pls"}).find("div", attrs={"class": "pi"}).find("strong").find("a").text
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
                           imgs = div.find("td", attrs={"class": "plc"}).find("div",attrs={"class":"pcb"}).find("table").findAll("img")
                           for img in imgs:
                                img.replaceWith(img.prettify())
                           c_item["txt"] = div.find("td", attrs={"class": "plc"}).find("div",attrs={"class":"pcb"}).find("table").text.replace("<br />", " ").replace("\r\n", "$*huanhang*$").replace("\"", "‘")
                           c_item["txt_len"] = len(c_item["txt"])
                           for key,value in c_item.items():
                              item['articles'] = item['articles'] + "\"%s\":\"%s\"" % (key, value)+","
                           item['articles'] += '\n'
                       except Exception as inst:
                           pass
                    try:
                      url1 = new_root.find("div",attrs={"class":"pgs mbm eis_plr cl"}).find("div",attrs={"class":"pg"}).find("a",attrs={"class":"nxt"}).get("href")
                      url = "http://www.redhongan.com/" + url1
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









