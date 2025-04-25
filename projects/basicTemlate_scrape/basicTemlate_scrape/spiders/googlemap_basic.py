import scrapy


class GooglemapBasicSpider(scrapy.Spider):
    name = 'googlemap_basic'
    allowed_domains = ['google.co.jp']
    start_urls = ['https://www.google.co.jp/maps/?hl=ja']

    def parse(self, response):
        pass
