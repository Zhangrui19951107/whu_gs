#coding=UTF-8
'''
Created on 2015年7月24日

@author: 龚兵
'''

from com.crawler.utils.logUntils import logUtil

import sys
import re
from com.crawler.utils import SpiderUtils
from com.crawler.utils.SpiderUtils import Tools
reload(sys)

sys.setdefaultencoding("utf8")  # @UndefinedVariable

import sys
if __name__ == '__main__':
#         log=logUtil.getLog()
# 
#         log.info("哈哈")
#         log.error("zzzzzzzzzz")
#    ÓëÑ¡µ÷ÉúÌ¸³É¹¦Ö®µÀ
#     s=u"aa"
#    # a = re.match('[ \u4e00 -\u9fa5]+',s)
#     re_han = re.compile(ur"([\u4E00-\u9FA5]+)", re.U)
#     # 开始使用findall
#     lis=re_han.findall(s) # 返回的是一个lis
#     print  lis # ['h', 'h', 'h', 'h', 'h']
#     if len(lis) == 0 :
#         print "aa"
#     else:
#         print "bb"
    #a="ÓëÑ¡µ÷ÉúÌ¸³É¹¦Ö®µÀ"
    a="aa"
    print Tools.isChinase(a)
   
#     if  == None:
#         print "A"+s
#     else :
#         print "b"


  #  print s
    
    