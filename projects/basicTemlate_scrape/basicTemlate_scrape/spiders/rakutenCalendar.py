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

def write_log(message):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

class RakutentravelCalendarSpider(scrapy.Spider):
    name = 'rakutenCalendar'
    allowed_domains = ['travel.rakuten.co.jp']
    
    def __init__(self, url=None, *args, **kwargs):
        super(RakutentravelCalendarSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            self.start_urls = ['https://travel.rakuten.co.jp/yado/shizuoka/higashi.html?lid=areaB_undated_izuhakone']
    
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=6,
                screenshot=False,
                callback=self.parse
            )

    def parse(self, response):
        hotels = response.xpath('//span[@class="checkPlanbtn"]')

        for hotel in hotels:
            url = hotel.xpath('.//a/@href').get()
            if url:
                if url.startswith("//"):
                    url = "https:" + url  # スキームを追加
                    
                yield SeleniumRequest(
                    url=url,
                    wait_time=5,
                    screenshot=False,
                    callback=self.parse_item
                )
                
        next_page = response.xpath('//a[@class="pagination__control-btn--next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        driver = response.meta['driver']
        url = response.url
        write_log(time.strftime('%Y/%m/%d %H:%M:%S'))
        write_log(url)
        # 前の画面が残ってしまう不具合対策。明示的にURLを再度開く
        driver.get(url)
        w = driver.execute_script('return document.body.scrollWidth')
        h = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(w, h)

        # 要素を取得
        title = response.xpath('//a[contains(@class, "rtconds") and contains(@class, "fn")]/text()').get()
        if not title:
            driver.save_screenshot("titleNg.png")
        write_log(covert_code(title))

        area = response.xpath('//*[@id="breadcrumbs-small"]/span/text()').get()
        if not area:
            driver.save_screenshot("areaNg.png")
        write_log(covert_code(area))

        plan = response.xpath('//ul[@class="htlPlnCsst mnmLstVw"]/li[1]/h4/text()').get()
        if not plan:
            driver.save_screenshot("planNg.png")
        write_log(covert_code(plan))

        room = response.xpath('//dd[@class="htlPlnTypTxt"]/h6[1]/text()').get()
        if not room:
            driver.save_screenshot("roomNg.png")
        write_log(covert_code(room))

        shokuji = response.xpath('string(//div[@class="htlPlnTypOpt"]/span[1])').get()
        if not shokuji:
            driver.save_screenshot("shokujiNg.png")
        shokuji_clean = shokuji.replace("食事", "").strip()
        write_log(covert_code(shokuji_clean))

        ninzu = response.xpath('string(//div[@class="htlPlnTypOpt"]/span[2])').get()
        if not ninzu:
            driver.save_screenshot("ninzuNg.png")
        ninzu_clean = ninzu.replace("人数", "").strip()
        write_log(covert_code(ninzu_clean))

        kingaku = response.xpath('//li[1][@data-locate="roomType-chargeByPerson-2"]//strong/text()').get()
        if not kingaku:
            driver.save_screenshot("kingakuNg.png")
        write_log(kingaku)

        if kingaku.find('~') == -1:
            idx = kingaku.find('円')
        else:
            idx = kingaku.find('~')
        kingaku_clear = kingaku[:idx]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        result = driver.find_elements(By.XPATH, '//a[@class="thickbox"]')
        for element in result:
            element.click()
            # iframeがロードされるのを待つ
            WebDriverWait(driver, 6).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "TB_iframeContent")))
            if click_element_by_xpath(driver,'//*[@id="calMonthPaging"]/li[3]/a'):
                write_log("Successfully clicked calMonthPaging")
                break
            else:
                # キーボードのESCキーを送る
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)            
                write_log("escapeKey")
                sleep(2)
                driver.save_screenshot("escapeKey.png")


        if click_element_by_xpath(driver,'//*[@id="calMonthPaging"]/li[3]/a'):
            write_log("Successfully clicked calMonthPaging")
        else:
            driver.save_screenshot("calMonthPagingClickNg.png")
            
        sleep(1)
        fullThiesMonth = driver.find_elements(By.XPATH, '//span[contains(@class, "full")]')
        if not fullThiesMonth:
            driver.save_screenshot("fullThisMonthNg.png")
        
        vacantThiesMonth = driver.find_elements(By.XPATH, '//span[contains(@class, "vacant")]')
        if not vacantThiesMonth:
            driver.save_screenshot("vacantThiesMonth.png")

        pastThiesMonth = driver.find_elements(By.XPATH, '//span[contains(@class, "past")]')
        if not pastThiesMonth:
            driver.save_screenshot("pastThisMonthNg.png")
            
            
        # 取得した要素の数を表示
        if fullThiesMonth:
            fullCountThiesMonth = len(fullThiesMonth)
        else:
            fullCountThiesMonth=0
        if vacantThiesMonth:
            vacantCountThiesMonth = len(vacantThiesMonth)
        else:
            vacantCountThiesMonth=0

        if pastThiesMonth:
            pastCountThiesMonth = len(pastThiesMonth)
        else:
            pastCountThiesMonth=0
            
        sleep(1)
        click_element_by_xpath(driver,'//*[@id="calMonthPaging"]/li[3]/a')
        sleep(1)
        click_element_by_xpath(driver,'//*[@id="calMonthPaging"]/li[3]/a')
        sleep(1)
        
        full = driver.find_elements(By.XPATH, '//span[contains(@class, "full")]')
        if not full:
            driver.save_screenshot("fullNg.png")
        vacant = driver.find_elements(By.XPATH, '//span[contains(@class, "vacant")]')
        if not vacant:
            driver.save_screenshot("vacantNg.png")
        past = driver.find_elements(By.XPATH, '//span[contains(@class, "past")]')
        if not past:
            driver.save_screenshot("pastNg.png")

        # 取得した要素の数を表示
        if full:
            fullCount = len(full)
        else:
            fullCount=0
        if vacant:
            vacantCount = len(vacant)
        else:
            vacantCount=0

        if past:
            pastCount = len(past)
        else:
            pastCount=0

        # キーボードのESCキーを送る
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)            
        # 元のコンテンツに戻る
        driver.switch_to.default_content()        

        write_log(time.strftime('%Y/%m/%d %H:%M:%S'))
        write_log("END")
        write_log("")
        write_log("")

        yield {
            'title': covert_code(title),
            'fullCount': fullCount,
            'vacantCount': vacantCount,
            'pastCount':pastCount,
            'fullCountThiesMonth': fullCountThiesMonth,
            'vacantCountThiesMonth': vacantCountThiesMonth,
            'pastCountThiesMonth':pastCountThiesMonth,
            'plan':covert_code(plan),
            'room':covert_code(room),
            'shokuji':covert_code(shokuji),
            'ninzu':covert_code(ninzu),
            'kingaku':covert_code(kingaku_clear),
            'URL':url,
            'area':area
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

# def click_element_by_xpath(driver, xpath, timeout=3):
#     # if not xpath:
#     #     driver.save_screenshot("screenshotName7.png")
#     #xpathで指定した項目を探して、click
#     xpathEle = driver.find_element(By.XPATH,xpath)
#     if xpathEle:
#         try:
#             xpathEle.click()
#             return True
#         except Exception as e:
#             return False
#     return False
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
            '\t': ''            
        })
        return code.translate(table)
    return code
