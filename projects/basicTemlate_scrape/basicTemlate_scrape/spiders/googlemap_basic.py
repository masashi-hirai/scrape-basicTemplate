import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import time
import re


class GooglemapBasicSpider(scrapy.Spider):
    name = 'googlemap_basic'
    allowed_domains = ['google.co.jp']
    start_urls = ['https://www.google.co.jp/maps/?hl=ja']

    def __init__(self, keyword=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.start_urls = ['https://www.google.co.jp/maps/?hl=ja']
        print(f"キーワード受け取り: {self.keyword}")    

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=6,
                screenshot=False,
                callback=self.parse
            )

    def parse(self, response):
        print(f"[DEBUG] response.meta keys: {response.meta.keys()}")        
        if 'driver' not in response.meta:
            print("[ERROR] Selenium driver not found in response.meta!")
            return
        driver = response.meta['driver']        
        
        url = response.url
        # 前の画面が残ってしまう不具合対策。明示的にURLを再度開く
        driver.get(url)

        #データ入力
        id = driver.find_element_by_id("searchboxinput")
        id.send_keys(self.keyword)
        id.send_keys(Keys.ENTER)

        time.sleep(6)

        scrollable_div = driver.find_element(By.XPATH, "//div[@role='feed']")

        previous_count = 0
        stable_count = 0

        for _ in range(3000):  # スクロール上限回数
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3)

            # 現在のアイテム数を取得
            items = driver.find_elements(By.XPATH, '//div[@role="feed"]//div[contains(@jsaction, "mouseover:pane")]')
            current_count = len(items)

            # 新しい要素が増えていないかチェック
            if current_count == previous_count:
                stable_count += 1
            else:
                stable_count = 0

            previous_count = current_count

            # 3回連続で変わらなければ「もう増えない」と判断して終了
            if stable_count >= 5:
                break

        w = driver.execute_script('return document.body.scrollWidth')
        h = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(w, h)
        driver.save_screenshot('scroll.png')

        items = []

        # select the Google Maps items
        maps_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="feed"]//div[contains(@jsaction, "mouseover:pane")]'))
        )

        for maps_item in maps_items:
            link_element = maps_item.find_element(By.CSS_SELECTOR, "a[jsaction][jslog]")
            url = link_element.get_attribute("href")
            try:
                title = maps_item.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall").text
            except:
                title = ""
            try:
                reviews_string = maps_item.find_element(By.CSS_SELECTOR, "span[role='img']").get_attribute("aria-label")
                reviews_string = covert_code(reviews_string)
                numbers = re.findall(r'\d+(?:\.\d+)?', reviews_string)
            except:
                numbers = [None, None]

            # 追加情報：住所
            try:
                address_element = maps_item.find_element(By.XPATH, './/div[contains(text(), "〒")]')  # 日本の住所表記（郵便番号）狙い
                address = address_element.text
            except:
                address = ""

            # 追加情報：価格帯（¥記号を含む）
            try:
                price_element = maps_item.find_element(By.XPATH, './/div[contains(text(), "￥")]')
                price = price_element.text
            except:
                price = ""

            # 正規表現で数値（小数と整数の両方）を抽出
            numbers = re.findall(r'\d+(?:\.\d+)?', reviews_string)                
                
            yield {
                'Keys':self.keyword,
                'title': covert_code(title),                
                'reviews_stars': numbers[0] if numbers else None,                
                'reviews_count': numbers[1] if numbers else None,
                'address': address,
                'price': covert_code(price),
                'URL': url
            }
        


def covert_code(code):
    if code:
        table = str.maketrans({
            '\u3000': '',
            ' ': '',
            '\r': '',
            '\n': '',
            '\t': '',
            ',': '' ,           
            '￥': '' ,           
            '万': ''           
        })
        return code.translate(table)
    return code

def write_log(message):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

from selenium.webdriver.common.by import By
def click_element_by_xpath(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    return element  # 要素を戻す


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

import traceback
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

