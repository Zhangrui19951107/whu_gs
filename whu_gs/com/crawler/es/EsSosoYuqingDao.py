#coding=UTF-8
'''
Created on 2015年8月3日

@author: gongbing
@说明: 搜索操作
'''
from elasticsearch.client import Elasticsearch
from elasticsearch.transport import Transport
from com.crawler.models.ContentModel import Content
import com.crawler.fx.wrok1 as fenci

class SoSoImp(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.es = Elasticsearch(['192.168.2.129', '192.168.2.130'])

        '''
        Constructor
        '''
    
    '''
         添加搜索信息
    '''
    def addSoso(self,Content):
        
        title=""
        if Content.title !=None:
            title = Content.title
            
        txt =""
        if Content.txt != None :
            txt = Content.txt
            
            #获取情感
        source=fenci.mm(title,txt)

         
        body={"title":Content.title,"summary":Content.summary,"context":Content.txt,"site_cls":Content.site_cls,"domaintype":Content.domaintype,
               "countryid":Content.countryid,"province":Content.province,"city":Content.city,"area":Content.area,"url":Content.url,"publictime":Content.pubdate,
               "createtime":Content.created,"sitename":Content.site_name,"domain1":Content.domain_1,"domain2":Content.domain_2,"sentiment":source,
               "subname":Content.subname}
         
        self.es.index(index="yuqing", doc_type="yuqing_type", body=body, id=Content.rowkey)
        
        #es.
         
        
    
        