#encoding=utf-8
#User: yuanjianfaith@msn.cn
#Date: 15-7-21
#Time: 下午3:30
#Desc: 网站爬取执行记录表
class Tb_craler_log(object):

    '''
        log_id      id
        source_id   来源id
        classify_id 版块id
        start_time  爬虫开始执行时间
        end_time    爬虫结束执行时间
        c_count     抓取数据的总数
        s_count     匹配上的总数
        createtime  创建时间
        updatetime  更新时间
        tag         备注
    '''

    def __init__(self,log_id =None,source_id =None,classify_id =None,
               start_time =None,end_time =None,c_count =None,s_count = None,
               createtime =None,updatetime = None,tag = None):

        self.log_id = log_id
        self.source_id = source_id
        self.classify_id = classify_id
        self.start_time = start_time
        self.end_time = end_time
        self.c_count = c_count
        self.s_count = s_count
        self.createtime = createtime
        self.updatetime = updatetime
        self.tag = tag


    def __setattr__(self, key, value):
        return object.__setattr__(self,key,value)


    def __getattr__(self, key):
        return self.__getattr__(key)

