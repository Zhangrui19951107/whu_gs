#encoding: utf-8
import codecs
import json
from logging import log
import socket

__author__ = 'bohaohan'
from datetime import datetime, date
import time
import requests
from BeautifulSoup import BeautifulSoup as bs
import sys
from items import FenghuoItem

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.cntongshan.com/News/NewsList-0-2.html'
last_t = date_t = datetime(2015, 7, 21, 23, 23)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def check_spider():
    new = 0
    page = 1
    while new > 20:
        new = 0
        r = requests.get(url)
        root = bs(r.text)
        page += 1
        url = "http://www.cntongshan.com/News/NewsList-0-2-AA-p" + str(page) + ".html"

        uls = root.find("div", attrs={"class": "ListMain"}).findAll("ul", attrs={"class": "l_l"})
        for ul in uls:
            lis = ul.findAll("li")
            for li in lis:
                div = li.find("div")
                curl = div.find("a").get("href")
                li.find("div").clear()
                datestr = li.text
                month = datestr[:datestr.index("月")]
                day = datestr[datestr.index("月") + 1:datestr.index("日")]
                hour = datestr[datestr.index("日") + 2:datestr.index(":")]
                minute = datestr[datestr.index(":") + 1:]
                date_t = datetime(2015, int(month), int(day), int(hour), int(minute))
                if date_t > last_t:
                    new += 1
                    print date_t
                    spider_cnts(curl)

def spider_cnts(url):
    print 'Hi, this is an item page! ', url
    item = FenghuoItem()
    r = requests.get(url)
    root = bs(r.text)
    # try:
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
    item["forumurl"] = root.find("a", attrs={"class": "A", "target": "_blank"}).get("href")
    item["site_type"] = '新闻'
    item["url"] = url
    url = url
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
    item["snatch_time"] = datetime.now()
    line = json.dumps(dict(item), cls=CJsonEncoder) + '\n'
    print line
    # except:
    #     #errors are log in error1.json with url
    #     line = url + "\n"
    #     file = codecs.open('error1.json', 'ab', encoding='utf-8')
    #     file.write(line.decode("unicode_escape"))
    #     pass

check_spider()