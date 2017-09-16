#coding=UTF-8
'''
Created on 2015年7月26日

@author: 龚兵
@说明： 任务model
'''

class Tb_Task(object):
    '''
    classdocs
    '''
    '''
       id : id号
       classify_id :分类id
       url :任务url
       urlType :url类型
       priority :任务优先级别
       status :任务状态
       updatetime :修改时间
       createtime : 创建时间
       tag :备注
         
    '''

    def __init__(self, id=None, classify_id=None, url=None, urlType=None,
               priority=None, status=None, updatetime=None, createtime=None, tag=None):

            self.id = id
            self.classify_id = classify_id
            self.url = url
            self.urlType = urlType
            self.priority = priority
            self.status = status
            self.updatetime = updatetime
            self.createtime = createtime
            self.tag = tag

    
    def __setattr__(self, key, value):
            return object.__setattr__(self, key, value)       
  


    def __getattr__(self, key):
            return self.__getattr__(key)


   
        