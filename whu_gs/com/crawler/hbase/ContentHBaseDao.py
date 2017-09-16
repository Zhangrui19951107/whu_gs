# coding=UTF-8
'''
Created on 2015年7月30日

@author: gongbing
@说明: hbase 数据库操作
'''
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import Mutation
from com.crawler.utils.BaseDB import BaseDB
from com.crawler.models.ContentModel import Content
import time


class ContentHBaseDaoImp(BaseDB):
    '''
    classdocs
    '''
    YUQINGCONTEXT_TB = "yuqingContext"
    
    def __init__(self):
        BaseDB.__init__(self)
       # super(BaseDB, self).__init__()
        
        print self.hbaseip
#         transport = TSocket.TSocket(self.hbaseip, self.hbasePort);
# 
#         transport = TTransport.TBufferedTransport(transport)
# 
#         protocol = TBinaryProtocol.TBinaryProtocol(transport);
# 
#         self.client = Hbase.Client(protocol)
# 
#         transport.open()        
    
    '''
      内容表  
    '''
    
    '''
     添加数据到数据库中
    '''
    def saveContentModel(self, Content):
        
        transport = TSocket.TSocket(self.hbaseip, self.hbasePort);

        transport = TTransport.TBufferedTransport(transport)

        protocol = TBinaryProtocol.TBinaryProtocol(transport);

        self.client = Hbase.Client(protocol)

        transport.open()        
        
        title = ""
        if Content.title != None :
            title = Content.title.encode('utf-8')
           
        subname = ""
        if Content.subname != None :
            subname = Content.subname.encode('utf-8')
            
        txt = ""
        if Content.txt != None :
            txt = Content.txt.encode('utf-8') 
        
#         author = None
#         if Content.has_key("author") :
#             author = Content.author.encode('utf-8') 
            
#         pubdate = None
#         if Content.has_key("pubdate") :
#             pubdate = Content.pubdate.encode('utf-8')        
        
            

        mutations = [Mutation(column="ctext:site_id", value=Content.site_id),
                    Mutation(column="ctext:website_id", value=Content.website_id),
                     Mutation(column="ctext:site_name", value=Content.site_name),
                     Mutation(column="ctext:site_url", value=Content.site_url),
                     Mutation(column="ctext:site_type", value=Content.site_type),
                     Mutation(column="ctext:site_cls", value=Content.site_cls),
                      Mutation(column="ctext:title", value=title),
                     Mutation(column="ctext:url", value=Content.url),
                     Mutation(column="ctext:view", value=Content.view),
                     Mutation(column="ctext:reply", value=Content.reply),
                     Mutation(column="ctext:author", value=Content.author),
                      Mutation(column="ctext:subname", value=subname),
                    Mutation(column="ctext:pubdate", value=Content.pubdate),
                       Mutation(column="ctext:created", value=Content.created),
                     Mutation(column="ctext:snatch_time", value=Content.snatch_time),
                     Mutation(column="ctext:domain_1", value=Content.domain_1),
                     Mutation(column="ctext:domain_2", value=Content.domain_2),
                      Mutation(column="ctext:txt_len", value=Content.txt_len),
                     Mutation(column="ctext:txt", value=txt),
                     Mutation(column="ctext:site_weight", value=Content.site_weight),
                      Mutation(column="ctext:ip", value=Content.ip),
                      Mutation(column="ctext:summary", value=Content.summary),
                     Mutation(column="ctext:topictype", value=Content.topictype),
                     Mutation(column="ctext:updatetime", value=Content.updatetime),
                    Mutation(column="ctext:domaintype", value=Content.domaintype),
                    Mutation(column="ctext:postip", value=Content.postip),
                    Mutation(column="ctext:postfloor", value=Content.postfloor),
                    Mutation(column="ctext:userid", value=Content.userid),
                    Mutation(column="ctext:userpage", value=Content.userpage),
                    Mutation(column="ctext:insertTime", value=str(int(time.time()) * 1000)),
                     Mutation(column="ctext:countryid", value=Content.countryid),
                    Mutation(column="ctext:province", value=Content.province),
                    Mutation(column="ctext:city", value=Content.city),
                    Mutation(column="ctext:area", value=Content.area),
                    Mutation(column="ctext:topPost", value=Content.topPost)
                    ]
          
        self.client.mutateRow(self.YUQINGCONTEXT_TB, Content.rowkey, mutations, None)
        
        transport.close()
        
        
