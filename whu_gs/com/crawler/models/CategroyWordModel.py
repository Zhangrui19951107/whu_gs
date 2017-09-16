#coding=UTF-8
'''
Created on 2015年7月20日

@author: zxh
@说明: 关键词model
'''

class CategroyWord(object):
    '''
    classdocs
        word_id :词id
        word:词名称
        weight:权重
        wordtype:词类型
        status:状态
        createtime:创建时间
        updatetime:修改时间
        tag:备注
    '''
    def __init__(self,word_id=None,word=None,weight=None,wordtype=None,status=None,createtime=None,updatetime=None,tag=None):  
            self.word_id=word_id
            self.word=word  
            self.weight=weight  
            self.wordtype=wordtype  
            self.status=status  
            self.createtime=createtime  
            self.updatetime=updatetime 
            self.tag=tag
    
    
    def __setattr__(self, key,value ):
            return object.__setattr__(self, key,value)       
  


    def __getattr__(self, key):
            return self.__getattr__(key)
