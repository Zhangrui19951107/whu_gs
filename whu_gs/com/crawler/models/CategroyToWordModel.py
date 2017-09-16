#coding=UTF-8
'''
Created on 2015年7月20日

@author: zxh
@说明: 行业类目关键词映射model
'''

class CategroyToWord(object):
    '''
    classdocs
        c_word_id :映射关系Id
        category_id:行业类目Id
        status:状态
        word_id:关键词Id
        createtime:创建时间
        updatetime:修改时间
        tag:备注
    '''
    def __init__(self,c_word_id=None,category_id=None,status=None,word_id=None,createtime=None,updatetime=None,tag=None):  
            self.c_word_id=c_word_id
            self.category_id=category_id  
            self.status=status  
            self.word_id=word_id  
            self.createtime=createtime  
            self.updatetime=updatetime 
            self.tag=tag
    
    
    def __setattr__(self, key,value ):
            return object.__setattr__(self, key,value)       
  


    def __getattr__(self, key):
            return self.__getattr__(key)
