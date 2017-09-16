#coding=UTF-8
'''
Created on 2015年7月21日

@author: Administrator
'''
from com.crawler.dao.SiteDao import SiteDaoImp

sitedao=SiteDaoImp()

siteBean=sitedao.getSite("东楚网", "www.hsdcw.com")



print siteBean.site_url

