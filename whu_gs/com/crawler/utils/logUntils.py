#coding=UTF-8
'''
Created on 2015年7月24日

@author: Seeping_
@说明: log日志工具类
'''
import logging, logging.config

class logUtil:
    '''
    classdocs
    '''
    @staticmethod
    def getLog():
        logging.config.fileConfig("/home/zhangrui/whu_gs/whu_gs/config/logger.conf")
        return logging.getLogger()
        