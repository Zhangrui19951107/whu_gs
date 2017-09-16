#coding=UTF-8
'''
Created on 2015年7月26日

@author: 陈路遥
@说明 ：通山机构编制网 爬取      http://www.tsxbb.gov.cn/
'''

from scrapy.spiders.crawl import CrawlSpider
from BeautifulSoup import BeautifulSoup as bs

import re
import scrapy
from com.crawler.dao.TaskDao import TaskDaoImp
import uuid
import datetime
import socket
from com.crawler.utils.logUntils import logUtil
from spider.items import FenghuoItem
from com.crawler.dao.piplineSaveDao import PiplineSaveDaoImp
from _cffi_backend import string
reload(sys)
sys.setdefaultencoding('utf-8')

class tsxbb_Spider(CrawlSpider):
    name = "tsbzw"
    allowed_domains = ["tsxbb.gov.cn"]
    start_urls = ['http://www.tsxbb.gov.cn/zxdt/',
                  'http://www.tsxbb.gov.cn/jdjc/',
                  'http://www.tsxbb.gov.cn/tzgg1/',
                  'http://www.tsxbb.gov.cn/bzgl/',
                  'http://www.tsxbb.gov.cn/sydwgg/',
                  'http://www.tsxbb.gov.cn/zsjs/',
                  'http://www.tsxbb.gov.cn/rdzt/sydwgg/'
    ]

    dicurl={"http://www.tsxbb.gov.cn/zxdt/":"1","http://www.tsxbb.gov.cn/jdjc/":"2",
            "http://www.tsxbb.gov.cn/tzgg1/":"3","http://www.tsxbb.gov.cn/bzgl/":"4",
            "http://www.tsxbb.gov.cn/sydwgg/":"5","http://www.tsxbb.gov.cn/zsjs/":"6",
            "http://www.tsxbb.gov.cn/rdzt/sydwgg/":"7"}    


    task=TaskDaoImp()   

    def __init__(self):
        #对数据进行存储
        self.saveData=PiplineSaveDaoImp()

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
        count = int(pageText)

        if int(pageText) > 0:
        	url = response.url + "index.html"
        	yield scrapy.Request(url, self.parse_page,  meta={'forumurl': url,"modelurl":response.url,"i":0,"count":int(pageText)})


    def parse_page(self, response):
        '''
        从各个页数获取相应新闻页面的url
        :param response:
        :return:
        '''
        root = bs(response.body)
        urls = root.findAll("a", attrs={"href": re.compile("^\./20")})
        forumurl = response.meta['forumurl']
        modelurl=response.meta['modelurl']
        modelid=self.dicurl.get(modelurl)

        urlset=set()
        for url in urls:
            url = url.get("href")
            url = url[1:]

            url = modelurl + url
            if self.task.getIsUrlByUrl(url) == False :
                urlset.add(url)
# #             #验证，如果任务数据中set数据为空，为不为空，对任务进行存储，并执行下一页
        saveListUrl = list()
        if len(urlset) > 0 :
                for u in urlset:
                    saveurl = (str(uuid.uuid1()),modelid,u,'html',1,'nostart')
                    saveListUrl.append(saveurl)
#                  
#                 #保存到数据库中    
                self.task.saveTaskList(saveListUrl)
#                 #进行下一页抓取
#                 #数据总页数
                count=response.meta['count']
# 
                i=response.meta['i']
                i=int(i)+1
                if i < int(count) :
                    infou = modelurl + "index_" + str(i) + ".html"
                    yield scrapy.FormRequest(infou, self.parse_page, meta={'forumurl': url,"modelurl":modelurl,"i":i,"count":int(count)})
                else :
                        #最后一夜
                    listBean=self.task.getTaskStatusByClassifyId(modelid, "nostart")
                    for Tb_Task in listBean :
                        yield scrapy.Request(Tb_Task.url, self.parse_item, meta={'forumurl': modelurl,"task_id":Tb_Task.id})
        else :
            
                #数据为空，证明没有新任务进行抓取了，就爬取新闻
            listBean=self.task.getTaskStatusByClassifyId(modelid, "nostart")
            for Tb_Task in listBean :
                yield scrapy.Request(Tb_Task.url, self.parse_item, meta={'forumurl': modelurl,"task_id":Tb_Task.id})
            
       



           

    def parse_item(self, response):
        '''
        访问各新闻页面，获取各键值
        :param response:
        :return:
        '''
        logUtil.getLog().info('news url :%s' % response.url)

        item = FenghuoItem()
        root = bs(response.body)
        item['topPost'] = "1"
        item["site_id"] = "13"
        item['website_id'] = ''
        item["site_name"] = '通山县机构编制网'
        item["area"] = "958"
        item["site_weight"] = "2"
        item['countryid'] = "1156"
        item['province'] = "1673"
        item['city'] = "136"
        item["ip"] = socket.gethostbyname("www.tsxbb.gov.cn")
        item["site_url"] = "www.tsxbb.gov.cn"
        item["forumurl"] = response.meta['forumurl']
        item["site_cls"] = '1'
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
        item["domain_2"] = ""
        item["snatch_time"] = datetime.datetime.now().__format__("")

        item["task_id"]=response.meta['task_id']
        self.saveData.saveContext(item)