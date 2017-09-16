#coding=UTF-8
'''
Created on 2015年7月22日

@author: 龚兵
@说明 ：自定义异常处理类
'''

class SystemException(Exception):
    '''
    classdocs
    '''

       
        
    def __init__(self,message=None,throwable=None):
        Exception.__init__(self,throwable)
       # self.t=
        self.message = message
        
    def __str__(self):
        return self.message;":\n";


        