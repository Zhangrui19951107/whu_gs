#coding=UTF-8
'''
Created on 2015年7月27日

@author: gongbing
@说明:
'''
from com.crawler.dao.TaskDao import TaskDaoImp

task=TaskDaoImp()

t=task.getIsUrlByUrl("http://www.jyxbb.gov.cn/zxdt//201507/t20150716_35032.html")
 
print t

# list=task.getTaskStatusByClassifyId("1", "nostart")
# 
# print list
