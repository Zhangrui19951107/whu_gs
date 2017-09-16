#coding=UTF-8
'''
Created on 2015年7月20日

@author: zxh
@说明: 新闻内容表model
'''

class Content(object):
    '''
    classdocs
        rowkey :主键列
        site_id:站点id
        website_id:来源网站id
        site_name:站点名称
        site_url:站点url
        site_type:站点类型   新闻、微博、视频等
        site_cls:站点行业  财经 娱乐等
        title:标题
        url:URL
        view:点击量
        reply:回复量
        author:作者
        subname:版块名称
        pubdate:发布时间
        snatch_time:抓取时间
        created:记录的创建时间
        domain_1:顶级域名
        domain_2:二级域名
        txt_len:全文长度
        txt:文章全文 
        site_weight:站点权重
        countryid:国家id
        province:省id
        city:市id
        area:区id
        ip:网站ip
        summary:摘要
        topictype:帖子类型
        updatetime:最后一楼发帖时间
        forumurl:版块url
        domaintype:境内外站点
        postip:发帖人ip
        postfloor:楼层
        userid:用户id
        userpage:发表人的个人首页
        topPost:是否是首贴
        website_name:站点名称
        annexs:附件的地址,多附件以分号隔开
    '''
    def __init__(self,rowkey=None,site_id=None,website_id=None,site_name=None,site_url=None,site_type=None,site_cls=None,
                 title=None,url=None,view=None,reply=None,author=None,subname=None,pubdate=None,
                 snatch_time=None,created=None,domain_1=None,domain_2=None,txt_len=None,
                 txt=None,site_weight=None,countryid=None,province=None,city=None,area=None,
                 ip=None,summary=None,topictype=None,updatetime=None,forumurl=None,
                 domaintype=None,postip=None,postfloor=None,userid=None,userpage=None,topPost=None,website_name=None,annexs=None):  
            self.rowkey=rowkey
            self.site_id=site_id  
            self.website_id=website_id  
            self.site_name=site_name  
            self.site_url=site_url  
            self.site_type=site_type 
            self.site_cls=site_cls
            self.title=title
            self.url=url  
            self.view=view  
            self.reply=reply  
            self.author=author  
            self.subname=subname 
            self.pubdate=pubdate
            self.snatch_time=snatch_time
            self.created=created  
            self.domain_1=domain_1  
            self.domain_2=domain_2  
            self.txt_len=txt_len  
            self.txt=txt 
            self.site_weight=site_weight
            self.countryid=countryid
            self.province=province  
            self.city=city  
            self.area=area  
            self.ip=ip  
            self.summary=summary 
            self.topictype=topictype
            self.updatetime=updatetime
            self.forumurl=forumurl  
            self.domaintype=domaintype  
            self.postip=postip  
            self.postfloor=postfloor  
            self.userid=userid 
            self.userpage=userpage
            self.topPost=topPost
            self.website_name=website_name
            self.annexs=annexs
    
    
    def __setattr__(self, key,value ):
            return object.__setattr__(self, key,value)       
  

    def __getattr__(self, key):
            return self.__getattr__(key)
