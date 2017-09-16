#coding=UTF-8
'''
Created on 2015年7月27日

@author: gongbing
'''
from com.crawler.dao.SiteClassifyDao import SiteClassfyDaoImp
from com.crawler.models.SiteClassifyModel import Tb_site_classify
import uuid
from com.crawler.dao.TaskDao import TaskDaoImp

classfy=SiteClassfyDaoImp()

tc=Tb_site_classify()
tc.site_id=33
tc.parent_id=0
tc.name="环保质量"
tc.forumurl="http://www.hahbj.com/huanbaozhiliang/index.html"
tc.actived=1
tc.cycle=60
tc.level=1
tc.urltype="html"
classfy.saveClassfily(tc)



# list=[('77133524-3400-11e5-83b6-240a649d058f', '1', 'http://www.jyxbb.gov.cn/zxdt/201307/t20130713_1647.html', 'html', 1, 'nostart')]
# 
# task = TaskDaoImp()
# task.saveTaskList(list)

