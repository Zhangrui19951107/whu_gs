#coding=utf-8
import re
import requests
from BeautifulSoup import BeautifulSoup as bs
__author__ = 'bohaohan'

import sys
from com.crawler.utils.BaseDB import BaseDB

reload(sys)
sys.setdefaultencoding('utf-8')

class UpdateTool(BaseDB):

    def getPubDate(self, site_url):
        conn = self.getConn()
        cur = conn.cursor()
        sql = "select pubdate from tb_content where site_url = %s order by pubdate desc"
        cur.execute(sql, (site_url))
        rows = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if rows == None:
            return "0"
        else:
            if str(rows["pubdate"]) == "None":
                return "0"
            else:
                return str(rows["pubdate"])

    def getUpdateTime(self, site_url):
        conn = self.getConn()
        cur = conn.cursor()
        sql = "select updatetime from tb_content where site_url = %s order by updatetime desc"
        cur.execute(sql, (site_url))
        rows = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if rows == None:
            return "0"
        else:
            if str(rows["updatetime"]) == "None":
                return "0"
            else:
                return str(rows["updatetime"])

    def hasUrl(self, url):
        iurl = url
        conn = self.getConn()
        cur = conn.cursor()
        # sql = "select url from tb_content where url = %s"
        sql = "select count(*) from tb_content where url = \'"
        sql = sql + iurl + "\'"
        n = cur.execute(sql)
        rows = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if rows["count(*)"]==0:
            return False
        else:
            return True

    def deleteContent(self, url):
        conn = self.getConn()
        cur = conn.cursor()
        sql = "delete from tb_content where url = %s"
        cur.execute(sql, (url))
        conn.commit()
        cur.close()
        conn.close()
