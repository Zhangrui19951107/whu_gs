# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#换行符 $*huanhang*$

class FenghuoItem(scrapy.Item):
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
        annexs:是否有附件
        website_name:站点名称
    '''
    # define the fields for your item here like:
    rowkey = scrapy.Field()
    url = scrapy.Field()
    parent_type = scrapy.Field()
    type = scrapy.Field() #模块
    title = scrapy.Field()
    author = scrapy.Field()
    view = scrapy.Field()
    domain_1 = scrapy.Field()
    domain_2 = scrapy.Field()
    news_id = scrapy.Field()
    reply = scrapy.Field()
    postfloor = scrapy.Field() #楼层数
    postid = scrapy.Field()
    updatetime = scrapy.Field()
    userid = scrapy.Field()
    userpage = scrapy.Field()
    rowkey = scrapy.Field()
    site_id = scrapy.Field()
    website_id = scrapy.Field()  
    site_name = scrapy.Field()
    site_url = scrapy.Field()
    site_type = scrapy.Field()
    site_cls = scrapy.Field()
    subname = scrapy.Field()
    pubdate = scrapy.Field()
    snatch_time = scrapy.Field()
    created = scrapy.Field()
    txt_len = scrapy.Field()  
    txt = scrapy.Field() 
    site_weight = scrapy.Field()
    countryid = scrapy.Field()
    province = scrapy.Field()  
    city = scrapy.Field()
    area = scrapy.Field()
    ip = scrapy.Field()
    summary = scrapy.Field()

    topictype = scrapy.Field()

    forumurl = scrapy.Field()
    domaintype = scrapy.Field()
    postip = scrapy.Field()
    topPost = scrapy.Field()

    articles = scrapy.Field()#楼层数组

    annexs = scrapy.Field()
    website_name = scrapy.Field()
    pass
