import sys
import os
from scrapy.crawler import CrawlerProcess

# scrapy.cftに記載のProject名.spiders.スパイダーのname　import スパイダーのクラス名
from basicTemlate_scrape.spiders.rakutenCalendar import RakutentravelCalendarSpider
from scrapy.utils.project import get_project_settings

sys.stdout = open('log.txt', 'w', encoding='utf-8')
sys.stderr = sys.stdout

# Scrapyプロジェクトのルート（scrapy.cfgがある場所）を明示的に指定
project_root = os.path.dirname(os.path.abspath(__file__))
os.environ['SCRAPY_SETTINGS_MODULE'] = 'basicTemlate_scrape.settings'
sys.path.append(project_root)

if __name__ == "__main__":
    print("スクレイピング開始")
    url = sys.argv[1] if len(sys.argv) > 1 else None

    from datetime import datetime
    # 日付を取得（例：'20250423'）
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    # ファイル名を組み立て
    file_name = f"output_RakutenCalendar_{date_str}"

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
    process.crawl(RakutentravelCalendarSpider, url=url)
    process.start()
