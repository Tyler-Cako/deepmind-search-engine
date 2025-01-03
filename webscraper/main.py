from crawler.Crawler import Crawler
import asyncio

crawler = Crawler()

async def main():
    await crawler.run("url_list.txt")

asyncio.run(main())