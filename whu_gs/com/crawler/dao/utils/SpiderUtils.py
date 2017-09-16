#coding=UTF-8
'''
Created on 2015年7月24日

@author: 龚兵
@说明: 项目工具类
'''
import time
import os
from logUntils import logUtil
import re

class Tools(object):
    '''
    classdocs
    '''
    
   
    J=10000
    OLDTIME=0
    TIMEZ=0
    
    '''
        获取新闻的rowkey
        staticmethod :静态函数
    '''
    @staticmethod
    def getContextRowKey():
#         global J
#         global OLDTIME
#         global TIMEZ

        #获取时间戳
        l= int(time.time())
        
        if Tools.J >= 20000 :
            J=10000
        
        if l == Tools.OLDTIME :
            Tools.TIMEZ=Tools.TIMEZ+1
        else :
            Tools.TIMEZ=0
            
        Tools.J=Tools.J+1
        
      
        rowkey=str(l)+"_"+str(Tools.TIMEZ)+"_"+str(Tools.J)
        
        return rowkey
    
    
    '''
            获取当前项目路径
    '''  
    loginfo=logUtil.getLog()
   
    @staticmethod
    def getProPath():
        thePath = os.getcwdu()
        Tools.loginfo.info(thePath)
        #截取字符串至项目名：crawlerSpider\
        thePath = thePath[:thePath.find("crawlerSpider\\")+len("crawlerSpider")]
        Tools.loginfo.info(thePath)
        return thePath
            
        '''
            判断是否为中文
       '''
    @staticmethod    
    def isChinase(text):
        re_han = re.compile(ur"([\u4E00-\u9FA5]+)", re.U)
        lis=re_han.findall(text)
        
        if len(lis) == 0 :
            return False
        else:
            return True
       # if list
       
    @staticmethod          
    def removeHtml(text): 
        text=text.replace_all("</br>", "\n").replace_all("<br>", "\n")
        
        
        
        

        