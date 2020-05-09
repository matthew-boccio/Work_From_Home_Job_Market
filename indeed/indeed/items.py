# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class IndeedItem(scrapy.Item):

    job_title = scrapy.Field() #check
    company_name = scrapy.Field() #check
    location = scrapy.Field() #check
    salary = scrapy.Field() #check
    job_type = scrapy.Field() #check
    remote = scrapy.Field() #check
    job_summary = scrapy.Field() #check
    job_headings_text = scrapy.Field() #check
    job_bullets_text = scrapy.Field() #check
    num_ratings = scrapy.Field() #check
    rating_out_of_5 = scrapy.Field() #check
    day_posted = scrapy.Field() #check
