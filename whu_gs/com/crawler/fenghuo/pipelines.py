# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs,json
import codecs , json
import datetime
from datetime import date, datetime
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class FenghuoPipeline(object):

    def __init__(self):
        # #save into json file
        self.file = codecs.open('baotw.json', 'wb', encoding='utf-8')
        #
        #save into mysql
        # create table news1(
        # news_id varchar(50) primary key,
        # url varchar(100),
        # title varchar(100)
        # )charset=utf8mb4;
        # self.dbpool = adbapi.ConnectionPool(
        #         'MySQLdb',
        #         db='test',
        #         host = '127.0.0.1',
        #         user='root',
        #         passwd='root',
        #         cursorclass=MySQLdb.cursors.DictCursor,
        #         charset='utf8',
        #         use_unicode=True
        # )

    def process_item(self, item, spider):

        #process file operation
        line = json.dumps(dict(item), cls=CJsonEncoder) + '\n'
        print line
        self.file.write(line.decode("unicode_escape"))

        #process mysql
        # query = self.dbpool.runInteraction(self._conditional_insert, item)
        # query.addErrback(self.handle_error,item = item)


        return item

    def _conditional_insert(self, tx, item):
        #news1 1000+
        #news2 800+
        tx.execute(\
            "insert into news1 (news_id, url, title)\
            values (%s, %s, %s)",

            (item['news_id'],
             item['url'],
             item['type'])

        )
    def handle_error(self, e, item):
        log.err(e)

        line = item['url'] + " " + str(e) + "\n"
        self.file = codecs.open('error.json', 'ab', encoding='utf-8')
        self.file.write(line.decode("unicode_escape"))