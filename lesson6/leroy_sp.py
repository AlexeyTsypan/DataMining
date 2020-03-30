# # -*- coding: utf-8 -*-
# import scrapy
#
#
# class LeroySpSpider(scrapy.Spider):
#     name = 'leroy_sp'
#     allowed_domains = ['novosibirsk.leroymerlin.ru']
#     start_urls = ['http://novosibirsk.leroymerlin.ru/catalogue/shlifovalnye-mashiny/']
#
#     def parse(self, response):
#         pass

import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyParserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroi'
    allowed_domains = ['novosibirsk.leroymerlin.ru']

    # start_urls = ['https://www.avito.ru/rossiya/kvartiry']  #https://www.avito.ru/rossiya?q=диван
    def __init__(self, search):
        self.start_urls = [f'https://novosibirsk.leroymerlin.ru/catalogue/{search}/']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//div[@class="hover-image-buttons"]//a[contains(@href, "product")]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        # photos = response.xpath('//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        # name = response.css('h1.title-info-title span.title-info-title-text::text').extract_first()
        # yield AvitoParserItem(name=name, photos=photos)
        loader = ItemLoader(item=LeroyParserItem(), response=response)
        loader.add_xpath('photos', '//picture//source[contains(@data-origin, "600")]/@data-origin')
        loader.add_xpath('name', "//h1[@class='header-2']/text()")
        loader.add_xpath('price', "//span[ @ slot = 'price']/text()")
        #pr_h = response.xpath("//dt/text()").extract()
        loader.add_xpath('pr_h','//div[@class="def-list__group"]//dt/text()')
        loader.add_xpath('pr_p', '//div[@class="def-list__group"]//dd/text()')


        # props = response.xpath("//div[@class='def-list__group']")
        # pr_h = props.xpath("//dt/text()").extract()
        # pr_p = props.xpath("//dd/text()").extract()
        # loader['pr_h'] = pr_h
        # loader['pr_p'] = pr_p

        # loader.add_css('name','h1.title-info-title span.title-info-title-text::text')
        yield loader.load_item()
