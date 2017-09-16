#coding=UTF-8
'''
Created on 2015年7月25日

@author: Administrator
'''
import time
import datetime
a=u'2015-05-21'
old = time.mktime(time.strptime(a,'%Y-%m-%d'))
nowTime = int(time.time())
print old
print nowTime