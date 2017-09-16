#coding=utf-8
'''
@author：Zetary-L
@introduction:function
'''

import MySQLdb
import ConfigParser
import datetime
import time
from math import *


#根据sitename从服务器读取数据求得权重
import DefaultInfo


def get_weight_by_sitename(sitename, whethermass, interval, now):
    conf = ConfigParser.ConfigParser()
    conf.read(DefaultInfo.HOME_DIR + "/db.cfg")
    db_ip = conf.get("mysql", "ip")
    db_user = conf.get("mysql", "user")
    db_pwd = conf.get("mysql", "pwd")
    db_name = conf.get("mysql", "db")
    conn = MySQLdb.connect(
        host=db_ip,
        user=db_user,
        passwd=db_pwd,
        db=db_name,
    )
    cursor = conn.cursor()
    # calc
    diclist = []
    diclist.append(dict(timenow=now - datetime.timedelta(days=1),frac=40))
    diclist.append(dict(timenow=now - datetime.timedelta(days=2),frac=30))
    diclist.append(dict(timenow=now - datetime.timedelta(days=7),frac=30))
    diclist.append(dict(timenow=now - datetime.timedelta(days=14),frac=20))
    bytes_ans = 0.0
    sitename = "%"+sitename+"%"
    for dic in diclist:
        timenow = dic['timenow']
        frac = dic['frac']
        begintime = timenow - datetime.timedelta(minutes=interval)
        begintimes = begintime.strftime("%Y-%m-%d %H:%M")
        endtime = timenow
        endtimes = endtime.strftime("%Y-%m-%d %H:%M")
        cursor.execute("SELECT COUNT(pubdate) FROM tb_content WHERE site_url like %s AND pubdate > %s AND pubdate < %s ",
                       (sitename, begintime, endtime))
        rows = cursor.fetchall()
        for row in rows:
            for r in row:
                bytes_ans += r*frac
    # end_calc
    bytes_ans = ceil(bytes_ans/100)+1
    cursor.close()
    conn.commit()
    conn.close()
    return ceil(bytes_ans)
