from crawler.Crawler import Crawler
from store.Store import Store
import certifi
import ssl

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

crawler = Crawler()
store = Store()

papers = crawler.run("url_list.txt")

store.insertPapers(papers)

print(f"Papers: {papers.keys()}")