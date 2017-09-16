#coding=UTF-8
'''
Created on 2015年7月20日

@author: 龚兵
@说明:   网站爬取执行记录 操作
'''
from com.crawler.utils.BaseDB import BaseDB
from com.crawler.models.CralerModels import Tb_craler_log
class CralerLogDaoImp(BaseDB):
    
    def saveCralerLog(self,Tb_craler_log):
        
        #获取数据库连接
        conn=self.getConn()
        cur = conn.cursor()
        
        sql = "insert into tb_craler_log(log_id,source_id,classify_id,start_time,end_time,c_count,)"

