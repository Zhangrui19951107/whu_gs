#encoding=utf-8
#User: yuanjianfaith@msn.cn
#Date: 15-7-20
#Time: 上午11:29
#Desc: 国内地域表

class China_area(object):

    '''
        area_id     地区id
        parent_id   父级id
        name        地名
        code        邮编
        zipCode     地区代码
        level       级别
        createtime  创建时间
        updatetime  更新时间
        tag         备注
    '''

    def __init_(self,area_id =None,parent_id =None,name =None,code =None,
               zipCode =None,level =None,createtime =None,updatetime =None,tag =None):

        self.area_id = area_id
        self.parent_id = parent_id
        self.name = name
        self.code = code
        self.zipCode = zipCode
        self.level = level
        self.createtime = createtime
        self.updatetime = updatetime
        self.tag = tag

    def __setattr__(self, key, value):
        return object.__setattr__(self,key,value)


    def __getattr__(self, key):
        return self.__getattr__(key)


