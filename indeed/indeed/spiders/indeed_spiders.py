from scrapy import Spider, Request
from indeed.items import IndeedItem
import re
import math

class IndeedSpider(Spider):
    name = 'indeed_spider'
    allowed_urls =['https://www.indeed.com']
    start_urls = ['https://www.indeed.com/jobs?l=United%20States&sort=date&remotejob=1']

    def parse(self, response):
        num_jobs = int(response.xpath('//div[@id="searchCountPages"]/text()').extract_first().strip().split(' ')[-2].replace(',',''))
        page_urls = [f'https://www.indeed.com/jobs?q&l=United%20States&sort=date&remotejob=1&start={i}' for i in range(0, 1000, 10)]
        #I did range 0 - 1000 because it looks like indeed has a 100 page search limit, and is zero indexed for the first page
        #items_per_page = 15 -> that's just a self reference

        for url in page_urls:
            yield Request(url = url, callback = self.parse_each_page)

    def parse_each_page(self, response):
        job_urls = response.xpath('//h2[@class="title"]/a/@href').extract()
        job_urls = ['https://www.indeed.com' + url for url in job_urls]

        # print('=' * 55)
        # print(len(job_urls))
        # print('=' * 55)
        #the above was just a test to see if things parsed properly

        for url in job_urls:
            yield Request(url=url, callback = self.parse_individual_job)

    def parse_individual_job(self, response):
            job_title = response.xpath('//h3[@class="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"]/text()').extract()
            company_name = response.xpath('//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]//text()').extract()[0]
            location = response.xpath('//div[@class="jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating"]/div').extract()[-1].replace('<div>', '').replace('</div>', '')
            salary = response.xpath('//span[@class="icl-u-xs-mr--xs"]/text()').extract_first()
            job_type = response.xpath('//span[@class="jobsearch-JobMetadataHeader-item  icl-u-xs-mt--xs"]/text()').extract_first()
            job_summary = response.xpath('//div[@class="jobsearch-jobDescriptionText"]//text()').extract()
            job_headings_text = response.xpath('//div[@class="jobsearch-jobDescriptionText"]/p/b//text()').extract()
            job_bullets_text = response.xpath('//div[@class="jobsearch-jobDescriptionText"]/ul/li/text()').extract()
            day_posted = response.xpath('//div[@class="jobsearch-JobMetadataFooter"]/text()').extract_first().replace(' - ', '')
            try:
                num_ratings = int(response.xpath('//div[@class="icl-Ratings icl-Ratings--gold icl-Ratings--sm"]/meta/@content').extract()[1])
            except Exception:
                num_ratings = 0
            try:
                rating_out_of_5 = float(response.xpath('//div[@class="icl-Ratings icl-Ratings--gold icl-Ratings--sm"]/meta/@content').extract()[0])
            except Exception:
                rating_out_of_5 = None


            item = IndeedItem()
            item['job_title'] = job_title
            item['company_name'] = company_name
            item['location'] = location
            item['salary'] = salary
            item['job_type'] = job_type
            item['job_summary'] = job_summary
            item['job_headings_text'] = job_headings_text
            item['job_bullets_text'] = job_bullets_text
            item['num_ratings'] = num_ratings
            item['rating_out_of_5'] = rating_out_of_5
            item['day_posted'] = day_posted

            yield item
