from crawler.Crawler import Crawler
import asyncio

crawler = Crawler()

async def main():
    papers = await crawler.run("url_list.txt")
    print(f"Papers found: {papers.keys()}")

asyncio.run(main())
