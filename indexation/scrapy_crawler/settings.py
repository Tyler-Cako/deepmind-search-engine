BOT_NAME = "scrapy_crawler"
SPIDER_MODULES = ["scrapy_crawler.spiders"]
NEWSPIDER_MODULE = "scrapy_crawler.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "scrapy_crawler.pipelines.SQLitePipeline": 300,
}