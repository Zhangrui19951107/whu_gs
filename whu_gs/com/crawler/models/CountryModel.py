#coding=UTF-8
'''
Created on 2015年7月20日

@author: 龚兵
@说明: 国家model
'''

class Country(object):
    '''
    classdocs
        country_id :国家id
        asscii:国家编码
        name:国家名称
        createtime:创建时间
        updatetime:修改时间
        tag:备注
    '''
    def __init__(self,country_id=None,asscii=None,name=None,createtime=None,updatetime=None,tag=None):  
            self.country_id=country_id
            self.asscii=asscii  
            self.name=name  
            self.createtime=createtime  
            self.updatetime=updatetime 
            self.tag=tag
    
    
    def __setattr__(self, key,value ):
            return object.__setattr__(self, key,value)       
  


    def __getattr__(self, key):
            return self.__getattr__(key)



   
        