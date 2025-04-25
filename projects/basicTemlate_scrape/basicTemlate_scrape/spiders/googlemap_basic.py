import scrapy


class GooglemapBasicSpider(scrapy.Spider):
    name = 'googlemap_basic'
    allowed_domains = ['google.co.jp']
    start_urls = ['https://www.google.co.jp/maps/?hl=ja']

    def parse(self, response):
        pass


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

