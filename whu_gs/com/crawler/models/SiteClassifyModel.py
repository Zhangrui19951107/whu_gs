#encoding=utf-8
#User: yuanjianfaith@msn.cn
#Date: 15-7-21
#Time: 下午3:21
#Desc: 原始分类表(版块表)
class Tb_site_classify(object):

    '''
        classify_id id
        site_id     站点id
        parent_id   父级id
        name        版块名称
        forumurl    版块url
        actived     是否激活
        cycle       网站抓取周期
        level       级别
        urltype     网站url展示数据类型
        createtime  创建时间
        updatetime  更新时间
        tag         备注
    '''

    def __init__(self,classify_id =None,site_id =None,parent_id =None,
               name =None,forumurl =None,actived =None,cycle = None,level =None,
               urltype =None,createtime =None,updatetime = None,tag = None):

        self.classify_id = classify_id
        self.site_id = site_id
        self.parent_id = parent_id
        self.name = name
        self.forumurl = forumurl
        self.actived = actived
        self.cycle = cycle
        self.level = level
        self.urltype = urltype
        self.createtime = createtime
        self.updatetime = updatetime
        self.tag = tag


    def __setattr__(self, key, value):
        return object.__setattr__(self,key,value)


    def __getattr__(self, key):
        return self.__getattr__(key)

