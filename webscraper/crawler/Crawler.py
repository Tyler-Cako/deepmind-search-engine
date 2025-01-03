import asyncio

import httpx
from .parser import parse



class Crawler(object):
    def __init__(self):
        self.papers = [] # List of papers found when crawling
        self.visited = set([]) # Set of visited URLs for traversal
        self.error_list = [] # List of URLs that were not parse-able

    async def run(self, path: str) -> None:
        """Start URL crawling given file path to a list of urls"""

        with open(path) as file:

            url = file.readline()
            # Read list of files from txt document
            while url:
                print(f"url: {url}")
                task = asyncio.create_task(self.crawlUrl(url.rstrip(), 10))
                await task
                url = file.readline()

    async def crawlUrl(self, url: str, counter: int) -> None:
        if url in self.visited:
            return
        
        async with httpx.AsyncClient() as client:
            self.visited.append(url)
            response = await client.get(url)
            responseHtml = response.text
            url_list, isPaper, error_list = parse(responseHtml)

            self.error_list.append(error_list)

            if isPaper:
                self.papers.append(responseHtml)

            for url in url_list:
                task = asyncio.create_task(self.crawlUrl(url, counter - 1))
                await task
