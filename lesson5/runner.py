from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from DataMining.lesson5.jobparser import settings
from DataMining.lesson5.jobparser.spiders.hhru import HhruSpider
from DataMining.lesson5.jobparser.spiders.sjru import SjruSpider
# from jobparser.spiders.sjru import SjruSpider


if __name__ =='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)
    process.start()
