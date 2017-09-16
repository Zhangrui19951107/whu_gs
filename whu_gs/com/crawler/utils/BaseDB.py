# coding=UTF-8
'''
Created on 2015年7月20日

@author: 龚兵
@说明: 数据库操作基础类
'''

import MySQLdb
import MySQLdb.cursors 
import ConfigParser
from com.crawler.utils.SpiderUtils import Tools
from com.crawler.utils.logUntils import logUtil

class BaseDB(object):
    '''
    classdocs
    '''
    hbaseip = None
    hbasePort = None
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read("/home/zhangrui/whu_gs/whu_gs/config/db.cfg")
        
        self.hbaseip = self.conf.get("hbase", "ip")
        self.hbasePort = self.conf.get("hbase","prot")
        

    '''
            获取数据库连接
    '''
        
    def getConn(self):
        return MySQLdb.connect(self.conf.get("mysql", "ip"), self.conf.get("mysql", "user"), self.conf.get("mysql", "pwd"), self.conf.get("mysql", "db"),cursorclass = MySQLdb.cursors.DictCursor,charset='utf8')


    '''
        关闭数据
    '''
    def closeConn(self, conn):
        if conn : 
            conn.close()
    
    
    


  
        
