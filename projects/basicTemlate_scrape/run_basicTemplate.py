import sys
import os
from scrapy.crawler import CrawlerProcess

# scrapy.cftに記載のProject名.spiders.スパイダーのname　import スパイダーのクラス名
from basicTemlate_scrape.spiders.googlemap_basic import GooglemapBasicSpider
from scrapy.utils.project import get_project_settings

sys.stdout = open('log.txt', 'w', encoding='utf-8')
sys.stderr = sys.stdout

if __name__ == "__main__":
    print("スクレイピング開始")

    # 起動引数を取得
    if len(sys.argv) >= 2:
        keyword = " ".join(sys.argv[1:])  # 複数引数を1つの文字列に
    else:
        keyword = "南足柄　公園"  # デフォルト値（なければエラーでもOK）


    from datetime import datetime
    # 日付を取得（例：'20250423'）
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    safe_keyword = keyword.replace(" ", "_").replace("\u3000", "_")
    # ファイル名を組み立て
    file_name = f"output_{safe_keyword}_{date_str}.csv"



    # 設定読み込み + 上書き
    settings = get_project_settings()
    settings.set("FEEDS", {
        f"output_{file_name}.csv": {
            "format": "csv",
            "encoding": "utf8",
            "overwrite": True
        }
    })


    process = CrawlerProcess(settings)
    process.crawl(GooglemapBasicSpider, keyword=keyword)
    process.start()
