# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from DataMining.lesson5.jobparser.items import JobparserItem
import re


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        # next_page = response.css("a.HH-Pager-Controls-Next::attr(href)")
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        # vacansy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)')

        for link in vac_list:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='bloko-header-1']/text()").extract()[0]
        salary_l = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        salary_min = 0
        salary_max = 0
        salary_cur = ''
        salary_desc = ''
        if len(salary_l)==1:
            salary_desc=salary_l[0]
        else:
            for s in salary_l:
                m = re.match('.*\d.*',s)
                if salary_min == 0 and m:
                    salary_min = int(re.sub(r'\D','',s))
                elif salary_min > 0 and m:
                    salary_max = int(re.sub(r'\D','',s))
                elif re.match(r'.*от|до.*', s):
                    salary_desc = ''
                elif re.match(r'.*руб.*', s):
                    salary_cur = 'руб'
                elif re.match(r'.*не указан.*', s):
                    salary_desc = s
                elif salary_cur=='':
                    salary_cur = s
                else:
                    salary_desc=s

        href = response.url
        source = self.allowed_domains

        yield JobparserItem(name=name, salary_min=salary_min,salary_max=salary_max,salary_cur=salary_cur,salary_desc=salary_desc, href=href,source=source)
