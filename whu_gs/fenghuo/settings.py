# -*- coding: utf-8 -*-

# Scrapy settings for fenghuo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'fenghuo'

SPIDER_MODULES = ['fenghuo.spiders']
NEWSPIDER_MODULE = 'fenghuo.spiders'


ITEM_PIPELINES = {
    'fenghuo.pipelines.FenghuoPipeline': 300
}

CONCURRENT_REQUESTS = 10000

COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    # 'Accept-Language': 'zh-CN,zh;q=0.8',
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fenghuo (+http://www.yourdomain.com)'
