import scrapy
import sched
from site import site as si
import time,datetime,json
from calc import *
import sites as sas 
import codecs

interval = 20
max_concurrency = 1000
now = datetime.datetime.now()
f = file("sites.json")
sl = json.load(f)
sl = sl["site"]
# schedule.enter(inc, 0, perform_command, (cmd, inc))
tochange_dict = dict()
for s in sl:
    site_now = si(name=s["name"], crawlername=s["crawlername"], limit=s["limit"], weight=get_weight_by_sitename(sitename=s["name"], whethermass=s["whethermass"], interval=interval, now=now),inuse=1)
    sas.sitelist.append(site_now)
for site in sitelist:
    site.pr()
sas.sitelist = allocate(sitelist=sas.sitelist,interval=interval, U=max_concurrency)
for site in sas.sitelist:
    tochange_dict[site.crawlername]=site.v
settings = get_project_settings()
settings.set("TO_CHANGE", tochange_dict)
proportion_dict = dict()
for site in sas.sitelist:
    proportion_dict[site.crawlername]=site.v
settings.set("SPIDER_PROPORTION", proportion_dict)