import scrapy
from scrapy.crawler import CrawlerProcess
settings = get_project_settings()
settings.set("TO_CHANGE", tochange_dict)
proportion_dict = dict()
for site in sas.sitelist:
    proportion_dict[site.crawlername] = site.v
settings.set("SPIDER_PROPORTION", proportion_dict)
print proportion_dict
process = CrawlerProcess(settings)
for site in sas.sitelist:
    process.crawl(site.crawlername)
print settings
process.start()