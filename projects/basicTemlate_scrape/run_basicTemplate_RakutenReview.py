import sys
import os
import traceback
from scrapy.crawler import CrawlerProcess

# scrapy.cftに記載のProject名.spiders.スパイダーのname　import スパイダーのクラス名
from basicTemlate_scrape.spiders.rakutenReview import RakutentravelReviewSpider

from scrapy.utils.project import get_project_settings

# 標準出力・標準エラー出力を log.txt にリダイレクト
sys.stdout = open('log.txt', 'w', encoding='utf-8')
sys.stderr = sys.stdout

# Scrapyプロジェクトのルート（scrapy.cfgがある場所）を明示的に指定
project_root = os.path.dirname(os.path.abspath(__file__))
os.environ['SCRAPY_SETTINGS_MODULE'] = 'basicTemlate_scrape.settings'
sys.path.append(project_root)

if __name__ == "__main__":
    try:
        print("スクレイピング開始")
        url = sys.argv[1] if len(sys.argv) > 1 else None

        from datetime import datetime
        # 日付を取得（例：'20250423_1430'）
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        # ファイル名を組み立て
        file_name = f"output_RakutenReview_{date_str}"

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
        process.crawl(RakutentravelReviewSpider, url=url)
        process.start()

    except Exception:
        # エラーが起きたら error_log.txt に出力
        with open("error_log.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        sys.exit(1)
