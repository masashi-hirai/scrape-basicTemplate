import scrapy
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import traceback
from selenium.common.exceptions import ElementClickInterceptedException


class JaranBasicSpider(scrapy.Spider):
    name = 'jaran'
    allowed_domains = ['jalan.net']
    
    def __init__(self, url=None, *args, **kwargs):
        super(JaranBasicSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            self.start_urls = ['https://www.jalan.net/kankou/150000/g1_22/?screenId=OUW3801&sortKbn=05']
    
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=6,
                screenshot=False,
                callback=self.parse
            )            

    def parse(self, response):
        # write_log(response.text)  # HTML の内容を表示
        items = response.xpath('//h3[contains(@class, "item-name rank-ico")]')            
        for hotel in items:
            url = hotel.xpath('.//a/@href').get()
            if url:
                yield response.follow(url, callback=self.parse_item)
        next_page = response.xpath('//p[@class="pagerLinks"]/a[contains(text(), "次へ")]/@href').get()
        write_log(f"next_page: {next_page}") 
        
        
        if next_page:
            write_log("次へ")
            write_log("")
            yield response.follow(next_page, callback=self.parse)
        else:
            write_log("次へなし")
            write_log("")
            
    def parse_item(self, response):
        url = response.url
        write_log(time.strftime('%Y/%m/%d %H:%M:%S'))
        write_log(url)
        # 前の画面が残ってしまう不具合対策。明示的にURLを再度開く

        # 要素を取得
        
        title = response.xpath('//h1[@class="detailTitle"]/text()').get()
        write_log(covert_code(title))

        area1 = response.xpath('//dl[@class="c-area"]/dd[1]/div/a/text()').get()
        write_log(covert_code(area1))

        area2 = response.xpath('//dl[@class="c-area"]/dd[2]/div/a/text()').get()
        write_log(covert_code(area2))

        area3 = response.xpath('//dl[@class="c-area"]/dd[3]/div/a/text()').get()
        write_log(covert_code(area3))

        area4 = response.xpath('//dl[@class="c-area"]/dd[4]/div/a/text()').get()
        write_log(covert_code(area4))

        category1 = response.xpath('//ul[@class="categoryList"]/li[1]/a/text()').get()
        write_log(covert_code(category1))

        category2 = response.xpath('//ul[@class="categoryList"]/li[2]/a/text()').get()
        write_log(covert_code(category2))

        reviewCount = response.xpath('//span[@class="reviewCount"]/a/b/text()').get()
        write_log(covert_code(reviewCount))


        categories = [
            ("manzoku", "manzokku.png"),
            ("yayamanzoku", "yayamanzokku.png"),
            ("hutu", "hutu.png"),
            ("yayahuman", "yayahuman.png")
        ]
        values = []
        for i, (var_name, screenshot) in enumerate(categories, start=1):
            value = response.xpath(f'//dl[@class="reviewRatingGraph__graph reviewRatingGraph__graph--bar"]//div[{i}]//span[@class="reviewRatingGraph__percentage"]/text()').get()
            if not value:
                values.append("-")
            else:
                write_log(covert_code(value))
                values.append(value)

        typeHyouka = [
            ("kozure", "kozure.png"),
            ("capple", "capple.png"),
            ("tomo", "tomo.png"),
            ("senior", "senior.png"),
            ("hitori", "hitori.png")
        ]
        hyoukas = []
        for i, var_name,in enumerate(typeHyouka, start=1):
            value = response.xpath(f'//dl[@class="reviewRatingGraph__graph reviewRatingGraph__graph--rating"]//div[{i}]//span[@class="reviewPoint"]/text()').get()
            if not value:
                hyoukas.append("-")
            else:
                write_log(covert_code(value))
                hyoukas.append(value)

        write_log(time.strftime('%Y/%m/%d %H:%M:%S'))
        write_log("END")

        write_log("")

        yield {
            'title': covert_code(title),
            'area1':covert_code(area1),
            'area2':covert_code(area2),
            'area3':covert_code(area3),
            'area4':covert_code(area4),
            'category1':covert_code(category1),
            'category2':covert_code(category2),
            'reviewCount':covert_code(reviewCount),
            'manzoku':covert_code(values[0]),
            'yayamanzoku':covert_code(values[1]),
            'futu':covert_code(values[2]),
            'yayafuman':covert_code(values[3]),
            'kozure':covert_code(hyoukas[0]),
            'caple':covert_code(hyoukas[1]),
            'tomo':covert_code(hyoukas[2]),
            'senior':covert_code(hyoukas[3]),
            'hitori':covert_code(hyoukas[4]),
            'URL':url,
        }


def click_element_by_class(driver, class_name, timeout=3):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, class_name))
        )
        scroll_and_click(driver, element)
        return True
    except Exception as e:
        write_log(f"Failed to click element with class '{class_name}': {e}")
        return False

def click_element_by_class2(driver, class_name, timeout=3):

        # 要素がクリック可能になるのを待つ
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, class_name))
        )
        if not element:
            driver.save_screenshot("screenshotName12.png")
            
        
        # スクロール位置を取得
        scroll_x = driver.execute_script("return window.pageXOffset;")
        scroll_y = driver.execute_script("return window.pageYOffset;")

        # 要素の中央座標を計算
        width = element.size['width']
        height = element.size['height']

        x_center = element.location['x'] + (width / 2) + scroll_x
        y_center = element.location['y'] + (height / 2) + scroll_y

        try:
            # JavaScript でクリック
            driver.execute_script("document.elementFromPoint(arguments[0], arguments[1]).click();", x_center, y_center)
            return True

        except Exception as e:
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(traceback.format_exc())  # エラーの詳細をファイルに書き込む
        #    print("エラーが発生しました。'log.txt' を確認してください。")
            return False


def click_element_by_id(driver, id_name, timeout=3):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, id_name))
        )
        scroll_and_click(driver, element)
        return True
    except Exception as e:
        write_log(f"Failed to click element with ID '{id_name}': {e}")
        return False


def click_element_by_id2(driver, id_name, timeout=3):

        # 要素がクリック可能になるのを待つ
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, id_name))
        )
        # if not element:
        #     driver.save_screenshot("screenshotName13.png")
            
        
        # スクロール位置を取得
        scroll_x = driver.execute_script("return window.pageXOffset;")
        scroll_y = driver.execute_script("return window.pageYOffset;")

        # 要素の中央座標を計算
        width = element.size['width']
        height = element.size['height']

        x_center = element.location['x'] + (width / 2) + scroll_x
        y_center = element.location['y'] + (height / 2) + scroll_y

        try:
            # JavaScript でクリック
            driver.execute_script("document.elementFromPoint(arguments[0], arguments[1]).click();", x_center, y_center)
            return True

        except Exception as e:
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(traceback.format_exc())  # エラーの詳細をファイルに書き込む
        #    print("エラーが発生しました。'log.txt' を確認してください。")
            return False


def click_element_by_name(driver, name_name, timeout=3):

        # 要素がクリック可能になるのを待つ
        element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.NAMENAME, name_name))
        )
        # if not element:
        #     driver.save_screenshot("screenshotName13.png")
            
        
        # スクロール位置を取得
        scroll_x = driver.execute_script("return window.pageXOffset;")
        scroll_y = driver.execute_script("return window.pageYOffset;")

        # 要素の中央座標を計算
        width = element.size['width']
        height = element.size['height']

        x_center = element.location['x'] + (width / 2) + scroll_x
        y_center = element.location['y'] + (height / 2) + scroll_y

        try:
            # JavaScript でクリック
            driver.execute_script("document.elementFromPoint(arguments[0], arguments[1]).click();", x_center, y_center)
            return True

        except Exception as e:
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(traceback.format_exc())  # エラーの詳細をファイルに書き込む
        #    print("エラーが発生しました。'log.txt' を確認してください。")
            return False

def click_element_by_xpath(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def scroll_and_click(driver, element):
    scroll_x = driver.execute_script("return window.pageXOffset;")
    scroll_y = driver.execute_script("return window.pageYOffset;")
    
    width = element.size['width']
    height = element.size['height']
    
    x_center = element.location['x'] + (width / 2) + scroll_x
    y_center = element.location['y'] + (height / 2) + scroll_y
    
    try:
        driver.execute_script(
            "document.elementFromPoint(arguments[0], arguments[1]).click();",
            x_center, y_center
        )
    except Exception as e:
        write_log(f"Failed to execute JavaScript click: {e}")

def covert_code(code):
    if code:
        table = str.maketrans({
            '\u3000': '',
            ' ': '',
            '\r': '',
            '\n': '',
            '\t': '',
            ',': ''            
        })
        return code.translate(table)
    return code

def write_log(message):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")
