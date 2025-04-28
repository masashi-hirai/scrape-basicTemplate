# Scrapy settings for basicTemlate_scrape project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'basicTemlate_scrape'

SPIDER_MODULES = ['basicTemlate_scrape.spiders']
NEWSPIDER_MODULE = 'basicTemlate_scrape.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'basicTemlate_scrape (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs



# ケース	DOWNLOAD_DELAY の目安
# 開発・テスト中	1〜2秒
# 軽い運用	2〜4秒
# 慎重な運用	5〜7秒（今のあなたの設定）
# 超安全志向	7秒以上 + AutoThrottle
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:

#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# --- 同一ドメインへの同時リクエスト数制限 ---
CONCURRENT_REQUESTS_PER_DOMAIN = 2  # 最大でも2つ同時まで（1ならさらにやさしい）

#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'basicTemlate_scrape.middlewares.BasictemlateScrapeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'basicTemlate_scrape.middlewares.BasictemlateScrapeDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'basicTemlate_scrape.pipelines.BasictemlateScrapePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# --- AutoThrottle機能：レスポンス速度に応じて自動調整 ---
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0     # 最初のリクエスト間隔（秒）
AUTOTHROTTLE_MAX_DELAY = 10.0      # 最大待機時間（秒）
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # 同時接続の目標数（1が人間っぽい）
AUTOTHROTTLE_DEBUG = False  # Trueにするとログに調整情報を表示




# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

from shutil import which

SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_EXECUTABLE_PATH = 'C:/Users/hhara/OneDrive/ドキュメント/work/reskiling/ScrapySpider_BasicTemplate/projects/basicTemlate_scrape/chromedriver.exe'
SELENIUM_DRIVER_ARGUMENTS=['-headless']  # '--headless' if using chrome instead of firefox
FEED_EXPORT_ENCODING ='utf-8'



# # --- リトライ設定（失敗時の自動リトライ） ---
# RETRY_ENABLED = True
# RETRY_TIMES = 3  # 最大リトライ回数
# RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# # --- リトライ時の待機時間（秒）---
# RETRY_DELAY = 5  # 5秒待ってからリトライ（アクセスしすぎを避ける）


# --- ログレベル（不要なら） ---
LOG_LEVEL = 'INFO'  # DEBUGだと大量に出るので注意