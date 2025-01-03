from crawler.Crawler import Crawler
<<<<<<< HEAD
import asyncio
=======
from store.Store import Store
import certifi
import ssl

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
>>>>>>> 99c3df7a9951e17ed97ea4a14c272171c13916a3

crawler = Crawler()
store = Store()

<<<<<<< HEAD
async def main():
    await crawler.run("url_list.txt")

asyncio.run(main())
=======
papers = crawler.run("url_list.txt")

store.insertPapers(papers)

print(f"Papers: {papers.keys()}")
>>>>>>> 99c3df7a9951e17ed97ea4a14c272171c13916a3
