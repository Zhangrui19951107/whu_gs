#coding=UTF-8
'''
Created on 2015年7月20日

@author: zxh
@说明: 行业类目model
'''

class Categroy(object):
    '''
    classdocs
        category_id :行业类目id
        parent_id:父级行业Id
        name:行业名称
        level:行业级别
        createtime:创建时间
        updatetime:修改时间
        tag:备注
    '''
    def __init__(self,category_id=None,parent_id=None,name=None,level=None,createtime=None,updatetime=None,tag=None):  
            self.country_id=category_id
            self.parent_id=parent_id  
            self.name=name  
            self.level=level  
            self.createtime=createtime  
            self.updatetime=updatetime 
            self.tag=tag
    
    
    def __setattr__(self, key,value ):
            return object.__setattr__(self, key,value)       
  


    def __getattr__(self, key):
            return self.__getattr__(key)
