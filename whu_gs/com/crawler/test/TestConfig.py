#coding=UTF-8
'''
Created on 2015年7月20日

@author: Administrator
'''


import ConfigParser

conf = ConfigParser.ConfigParser()
    
conf.read("../../../config/db.cfg")


print conf.get("mysql", "ip")
    
    