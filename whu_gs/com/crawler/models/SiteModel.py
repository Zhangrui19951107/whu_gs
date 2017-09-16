# encoding=utf-8
# User: yuanjianfaith@msn.cn
# Date: 15-7-21
# Time: 下午3:08
# Desc: 站点表
class Tb_site(object):

    '''
        site_id     站点id
        site_name   站点名称
        site_url    一级域名
        type        网站类型
        actived     是否激活
        parent_id   父级id
        domaintype  境内/境外
        country_id  国家id
        pro_id      省id
        city_id     市id
        area_id     区id
        language    站点语言
        weight      域名权重
        cycle       网站抓取周期
        createtime  创建时间
        updatetime  更新时间
        tag         备注
    '''

    def __init__(self, site_id=None, site_name=None, site_url=None, type=None,
               actived=None, domaintype=None, country_id=None, pro_id=None, city_id=None,
               area_id=None, language=None, weight=None, cycle=None, createtime=None,
               updatetime=None, tag=None):

            self.site_id = site_id
            self.site_name = site_name
            self.site_url = site_url
            self.type = type
            self.actived = actived
            self.domaintype = domaintype
            self.country_id = country_id
            self.pro_id = pro_id
            self.city_id = city_id
            self.area_id = area_id
            self.language = language
            self.weight = weight
            self.cycle = cycle
            self.createtime = createtime
            self.updatetime = updatetime
            self.tag = tag


    def __setattr__(self, key, value):
            return object.__setattr__(self, key, value)       
  


    def __getattr__(self, key):
            return self.__getattr__(key)


