from crawler.Crawler import Crawler
import certifi
import ssl

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

crawler = Crawler()

crawler.crawl("url_list.txt")