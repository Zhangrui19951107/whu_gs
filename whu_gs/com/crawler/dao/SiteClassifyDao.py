# coding=UTF-8
'''
Created on 2015年7月20日

@author: 龚兵
@说明:   原始分类数据库操作
'''
from com.crawler.utils.BaseDB import BaseDB
from com.crawler.models.SiteClassifyModel import Tb_site_classify
class SiteClassfyDaoImp(BaseDB):
    
    '''
              保存原始分类
    '''
    def saveClassfily(self, Tb_site_classify):
        
        conn = self.getConn();
        cur = conn.cursor()
        sql = "insert into tb_site_classify(site_id,parent_id,name,forumurl,actived,cycle,level,urltype,tag) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        
        cur.execute(sql, (Tb_site_classify.site_id, Tb_site_classify.parent_id, Tb_site_classify.name, Tb_site_classify.forumurl, Tb_site_classify.actived,Tb_site_classify.cycle,Tb_site_classify.level,Tb_site_classify.urltype,Tb_site_classify.tag));
        
        conn.commit()
        cur.close()
        conn.close()   
        
        
