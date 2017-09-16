#coding=UTF-8
'''
Created on 2015年7月22日

@author: 龚兵
'''
import logging  
import logging.handlers 

from com.crawler.exception.Exception import SystemException



b=Exception("zzzzzzzz")

e=SystemException("a",b)

logging.basicConfig(filename = 'd:/a.log', level = logging.DEBUG)

logging.debug(e)