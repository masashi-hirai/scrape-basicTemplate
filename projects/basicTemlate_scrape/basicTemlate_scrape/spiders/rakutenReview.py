import sys
import traceback
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import ElementClickInterceptedException

class RakutentravelReviewSpider(scrapy.Spider):
    name = 'rakutenReview'
    allowed_domains = ['travel.rakuten.co.jp']

    def __init__(self, url=None, *args, **kwargs):
        super(RakutentravelReviewSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            self.start_urls = ['https://travel.rakuten.co.jp/yado/shizuoka/shimoda.html?lid=areaB_undated_izuhakone']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=6,
                screenshot=False,
                callback=self.parse
            )

    def parse(self, response):
        hotels = response.xpath('//p[@class="cstmrEvl"]')

        for hotel in hotels:
            url = hotel.xpath('.//a/@href').get()
            if url:
                yield response.follow(url, callback=self.parse_item)

        next_page = response.xpath('//a[contains(@class, "pagination__control") and contains(text(), "次へ")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        main_hotel_info = response.xpath('//div[@class="header__hotel-info"]')
        url = main_hotel_info.xpath('.//a/@href').get()
        url = "https:" + url
        title = main_hotel_info.xpath('.//a[@class="rtconds fn"]/text()').get()
        review_count = main_hotel_info.xpath('.//ul/li[@class="review-count__wrapper"]/a/em/text()').get()

        comment_area = response.xpath('//div[@id="commentArea"]')
        for comment in comment_area.xpath('.//div[@class="commentBox"]'):
            yield {
                'title': self.covert_code(title),
                'reviewCount': self.convert_Comma(review_count),
                'user': self.covert_code(comment.xpath('.//span[@class="user"]/text()').get()),
                'rate': comment.xpath('.//p[@class="commentRate"]/span[contains(@class,"rate rate")]/text()').get(),
                'mokuteki': comment.xpath(".//dl[@class='commentPurpose']/dd[1]/text()").get(),
                'douhansha': comment.xpath(".//dl[@class='commentPurpose']/dd[2]/text()").get(),
                'nengappi': comment.xpath(".//dl[@class='commentPurpose']/dd[3]/text()").get(),
                'commentCustomer': self.covert_code(comment.xpath('.//dl[@class="commentReputation"]//p[@class="commentSentence"]/text()').get()),
                'commentHotel': self.covert_code(comment.xpath('.//dl[@class="commentHotel"]//p[@class="commentSentence"]/text()').get()),
                'plan1': self.covert_code(comment.xpath('.//dl/dd[@class="plan"]/a/text()').get()),
                'plan2': self.covert_code(comment.xpath('.//dl/dd[@class="plan"][2]/text()').get()),
                'URL': url
            }

        next_page2 = response.xpath('//li[@class="pagingNext"]/a/@href').get()
        if next_page2:
            yield response.follow(next_page2, callback=self.parse_item)

    def covert_code(self, code):
        if code:
            table = str.maketrans({
                '\u3000': '',  # 全角スペースを除去
                ' ': '',       # 半角スペースも除去
                '\r': '',      # 改行コードなども除去
                '\n': '',
                '\t': ''
            })
            return code.translate(table)
        return code

    def convert_Comma(self, review_count):
        if review_count:
            return int(review_count.replace(',', ''))
        return review_count

# ----------------------------
# ここからエラーキャッチ追加部分！
# ----------------------------
if __name__ == '__main__':
    try:
        from scrapy.crawler import CrawlerProcess

        process = CrawlerProcess(settings={
            'FEEDS': {
                'output.json': {'format': 'json'},
            },
        })
        process.crawl(RakutentravelReviewSpider)
        process.start()
    except Exception:
        with open("error_log.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        sys.exit(1)
