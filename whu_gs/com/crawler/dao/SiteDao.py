#coding=UTF-8
'''
Created on 2015年7月21日

@author: Administrator
'''
from com.crawler.utils.BaseDB import BaseDB
from com.crawler.models.SiteModel import Tb_site

class SiteDaoImp(BaseDB):
    '''
    classdocs
    '''



    '''
          通过站点名称，和站点的url 获取站点的所有信息
          reuturn :返回站点实体类
    '''
    def getSite(self,siteName,siteUrl):
        
        #获取数据库连接
        conn=self.getConn()
        
        cur = conn.cursor()
        sql = "select * from tb_site where site_name = %s and site_url=%s"
        

        cur.execute(sql,(siteName,siteUrl))
        
        rows = cur.fetchall()
        #print rows
        siteBean=Tb_site()
        for row in rows:
            siteBean.site_id=row['site_id']
            siteBean.site_name=row['site_name']
            siteBean.site_url=row['site_url']
            siteBean.type=row['type']
            siteBean.actived=row['actived']
            siteBean.domaintype=row['domaintype']
            siteBean.country_id=row['country_id']
            siteBean.pro_id=row['pro_id']
            siteBean.city_id=row['city_id']
            siteBean.area_id=row['area_id']
            siteBean.language=row['language']
            siteBean.weight=row['weight']
            siteBean.cycle=row['cycle']
            siteBean.createtime=row['createtime']
            siteBean.updatetime=row['updatetime']
            siteBean.tag=row['tag']


        cur.close()
        conn.close()
        
        return siteBean
        
        
    
        