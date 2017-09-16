#coding=UTF-8
from com.crawler.dao.TaskDao import TaskDaoImp
from com.crawler.utils.logUntils import logUtil
import time
from com.crawler.models.ContentModel import Content
from com.crawler.utils.SpiderUtils import Tools
from com.crawler.hbase.ContentHBaseDao import ContentHBaseDaoImp
from com.crawler.es.EsSosoYuqingDao import SoSoImp
from com.crawler.utils.TrashContextUtils import TrashContextTools


class PiplineSaveDaoImp(object):
    
    
    
    def __init__(self):
        self.task=TaskDaoImp()
        self.hbaseContext=ContentHBaseDaoImp()
        self.soso=SoSoImp()
   
    ''''
      保存新闻数据
    '''
    def saveContext(self,item):

        #新闻实体类
        newsBean=Content()
        item=dict(item)
        #rowkey
        newsBean.rowkey=Tools.getContextRowKey()
        if item.has_key('url') :
            newsBean.url=item['url']
        if item.has_key('site_id') :
            newsBean.site_id=item['site_id']
        if item.has_key('website_id') :
            newsBean.website_id=item['website_id']
        if item.has_key('website_name') :
            newsBean.website_name=item['website_name']
        
        if item.has_key('annexs') :
            newsBean.annexs=item['annexs']
        else:
            newsBean.annexs=""
        if item.has_key('site_name') :
            newsBean.site_name=item['site_name']
        if item.has_key('site_url') :
            newsBean.site_url=item['site_url']
        if item.has_key('site_cls') :    
            newsBean.site_cls=item['site_cls']
        if item.has_key('title') :    
            newsBean.title=item['title']
#          #newsBean.url=item['url']
        

        if item.has_key('view') :
            newsBean.view=item['view']
        else:
            newsBean.view=""

        if item.has_key('reply') :
            newsBean.reply=item['reply']
        else:
            newsBean.reply=""   
         
        if item.has_key('author') :
            newsBean.author=item['author']
        else:
            newsBean.author=""  
        if item.has_key('pubdate') :    
            newsBean.pubdate=item['pubdate']
        newsBean.created=str(int(time.time()))
        if item.has_key('snatch_time') :
            newsBean.snatch_time=item['snatch_time']
        if item.has_key('domain_1') :
            newsBean.domain_1=item['domain_1']
        if item.has_key('domain_2') :
            newsBean.domain_2=item['domain_2']
        if item.has_key('txt_len') :
            newsBean.txt_len=item['txt_len']
        if item.has_key('txt') :
            newsBean.txt=item['txt']
        if item.has_key('site_weight') :
            newsBean.site_weight=item['site_weight']
        if item.has_key('countryid') :
            newsBean.countryid=item['countryid']
        if item.has_key('province') :
            newsBean.province=item['province']
        if item.has_key('city') :
            newsBean.city=item['city']
        if item.has_key('area') :
            newsBean.area=item['area']
        if item.has_key('ip') :
            newsBean.ip=item['ip']
        
        if item.has_key('summary') :
            newsBean.summary=item['summary']
        else:
            newsBean.summary=""          
        
        if item.has_key('topictype') :
            newsBean.topictype=item['topictype']
        else:
            newsBean.topictype="0"   
#         newsBean.updatetime=item['updatetime']
        if item.has_key('forumurl') :
            newsBean.forumurl=item['forumurl']
        
        if item.has_key('domaintype') :
            newsBean.domaintype=item['domaintype']
        else:
            newsBean.domaintype="0"  
            

        if item.has_key('postip') :
            newsBean.postip=item['postip']
        else:
            newsBean.postip="0"     
                
        if item.has_key('postfloor') :
            newsBean.postfloor=item['postfloor']
        else:
            newsBean.postfloor="0"           
        
        if item.has_key('userid') :
            newsBean.userid=item['userid']
        else:
            newsBean.userid=""  
        
        if item.has_key('userpage') :
            newsBean.userpage=item['userpage']
        else:
            newsBean.userpage=""                   


        newsBean.topPost=item['topPost']
       
        #任务id
        task_id=None
        if item.has_key('task_id') :
            task_id = item["task_id"]
        

        try:
            
            #存储到es中
  #          self.soso.addSoso(newsBean)
            
            #对新闻数据进行存储
            if Tools.isChinase(newsBean.title):
                if TrashContextTools.isSaveByPublicTime(newsBean.pubdate) : 
                    self.hbaseContext.saveContentModel(newsBean)
                    self.soso.addSoso(newsBean)
                
            if task_id !=None :
                self.task.updateTaskStatusById(task_id, "success")
             
        except Exception,e:
            print e
            logUtil.getLog().error(e)        