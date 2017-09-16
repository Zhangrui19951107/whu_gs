#coding=UTF-8
'''
Created on 2015年7月21日

@author: Seeping_
'''
from com.crawler.dao.ContentDao import ContentDaoImp
from com.crawler.models.ContentModel import Content


c=ContentDaoImp()

model=Content()
model.rowkey="121"
# model.site_id= 1*1
# model.website_id=1
# model.site_name="wwww.baidu"
# model.site_url="bad"
# model.site_type=1
# model.site_cls=12
# model.title="11"
# model.url="wwwwwww"
# model.view=1212
# model.reply=11
# model.author="1212"
# model.subname="12121"
# model.pubdate="2015-05-10 01:00:00"
# model.snatch_time=1212121
# model.created=12132313
# model.domain_1="wwww"
# model.domain_2="111"
# model.txt_len=12
# model.txt="1111111111111111111111111"
# model.site_weight=2
# model.countryid=1
# model.province=1
# model.city=12
# model.area=123
# model.ip="121"
# model.summary=""
# model.topictype=1
# model.updatetime=121212
# model.forumurl=""
# model.domaintype=1
# model.postip=""
# model.postfloor=1
# model.userid=""
# model.topPost=1
# model.website_name="烽火"
# model.annexs="abc"

   
c.saveContentModel(model)
    
   
