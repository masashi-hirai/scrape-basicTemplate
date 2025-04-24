import scrapy


class GooglemapBasicSpider(scrapy.Spider):
    name = 'googlemap_basic'
    allowed_domains = ['www.google.co.jp/maps']
    start_urls = ['http://www.google.co.jp/maps/']

    def parse(self, response):
        pass
