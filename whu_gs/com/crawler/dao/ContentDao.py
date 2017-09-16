# coding=UTF-8
'''
Created on 2015年7月21日

@author: 龚兵
@说明: 新闻表数据库操作
'''
from models.ContentModel import Content
from utils.BaseDB import BaseDB
import MySQLdb

class ContentDaoImp(BaseDB):
    

    '''
         保存新闻数据
    '''
    def saveContentModel(self, Content):
        conn = self.getConn();
        cur = conn.cursor()
        
        sql = "insert into tb_content(rowkey,site_id,website_id,site_name,site_url,site_cls,site_type,title,url,view,reply,author,subname,pubdate,created,snatch_time,domain_1,domain_2,txt_len,txt,site_weight,countryid,province,city,area,ip,summary,topictype,updatetime,forumurl,domaintype,postip,postfloor,userid,userpage,topPost,website_name,annexs) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql, (Content.rowkey,Content.site_id,Content.website_id,Content.site_name,Content.site_url,Content.site_cls,Content.site_type,Content.title,Content.url,Content.view,Content.reply
                          ,Content.author,Content.subname,Content.pubdate,Content.created,Content.snatch_time,Content.domain_1,Content.domain_2,Content.txt_len,Content.txt,Content.site_weight,Content.countryid,Content.province,Content.city,Content.area,
                          Content.ip,Content.summary,Content.topictype,Content.updatetime,Content.forumurl,Content.domaintype,Content.postip,Content.postfloor,Content.userid,Content.userpage,Content.topPost,Content.website_name,Content.annexs));
        
        conn.commit()
        cur.close()
        conn.close()
    
#     def saveContent(self,FenghuoItem):
#         conn = self.getConn();
#         cur = conn.cursor()
#         sql = "insert into tb_content(rowkey,site_id,website_id,site_name,site_url,site_cls,site_type,title,url,view,reply,author,subname,pubdate,created,snatch_time,domain_1,domain_2,txt_len,txt,site_weight,countryid,province,city,area,ip,summary,topictype,updatetime,forumurl,domaintype,postip,postfloor,userid,userpage,topPost,website_name,annexs) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         cur.execute(sql, (FenghuoItem['rowkey'],FenghuoItem['site_id'],FenghuoItem['website_id'],FenghuoItem['site_name'],FenghuoItem['site_url'],FenghuoItem['site_cls'],FenghuoItem['site_type'],FenghuoItem['title'],FenghuoItem['url'],FenghuoItem['view'],FenghuoItem['reply']
#                           ,FenghuoItem['author'],FenghuoItem['subname'],FenghuoItem['pubdate'],FenghuoItem['created'],FenghuoItem['snatch_time'],FenghuoItem['domain_1'],FenghuoItem['domain_2'],FenghuoItem['txt_len'],FenghuoItem['txt'],FenghuoItem['site_weight'],FenghuoItem['countryid'],FenghuoItem['province'],FenghuoItem['city'],FenghuoItem['area'],
#                           FenghuoItem['ip'],FenghuoItem['summary'],FenghuoItem['topictype'],FenghuoItem['updatetime'],FenghuoItem['forumurl'],FenghuoItem['domaintype'],FenghuoItem['postip'],FenghuoItem['postfloor'],FenghuoItem['userid'],FenghuoItem['userpage'],FenghuoItem['topPost'],FenghuoItem['website_name'],FenghuoItem['annexs']));
#         
#         conn.commit()
#         cur.close()
#         conn.close()
