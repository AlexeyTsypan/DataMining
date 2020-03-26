# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from DataMining.lesson5.jobparser.items import JobparserItem
import re


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[contains(@class,'Dalshe')]/@href").extract_first()
        # next_page = response.css("a.HH-Pager-Controls-Next::attr(href)")
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath("//a[contains(@href,'vakansii')]/@href").extract()

        for link in vac_list:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@class]/text()").extract()[0]
        salary_l = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        salary_cur = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/span/text()").extract()
        if salary_cur:
            salary_cur = salary_cur[0]
        else:
            salary_cur = ''

        salary_min = 0
        salary_max = 0
        # salary_cur = ''
        salary_desc = ''
        if len(salary_l) == 1:
            salary_desc = salary_l[0]  # salary_l=re.split(r'\w+',salary_l)
        else:
            for s in salary_l:
                m = re.match('.*\d.*', s)
                if salary_min == 0 and m:
                    salary_min = int(re.sub(r'\D', '', s))
                elif salary_min > 0 and m:
                    salary_max = int(re.sub(r'\D', '', s))

        href = response.url
        source = self.allowed_domains

        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, salary_cur=salary_cur,
                            salary_desc=salary_desc, href=href,source=source)
