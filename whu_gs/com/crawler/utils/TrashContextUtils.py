#coding=UTF-8

'''
Created on 2015年8月7日

@author: gongbing
@s说明： 垃圾数据过滤
'''
import time

class TrashContextTools(object):
    '''
    classdocs
    '''


#     def __init__(self, params):
#         '''
#         Constructor
#         '''
        
    #把发布时间大于1周的数据去掉
    @staticmethod
    def isSaveByPublicTime(publicTime):
        
        publicTime=publicTime.split(" ")[0]
        
            #当前时间戳
        nowTime = int(time.time())
        
        old = time.mktime(time.strptime(publicTime,'%Y-%m-%d'))

        cha = nowTime - old 
        
        if cha < 604800 :
            return True
        else :
            return False
        