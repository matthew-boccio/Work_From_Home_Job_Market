# this is my items.py folder

import scrapy

class IndeedItem(scrapy.Item):

    job_title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    job_type = scrapy.Field()
    remote = scrapy.Field()
    job_summary = scrapy.Field()
