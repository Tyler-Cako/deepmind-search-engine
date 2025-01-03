import asyncio

import httpx
from .parser import HTMLParser

from typing import Dict


class Crawler(object):
    def __init__(self):
        self.papers = {} # Dict of papers found when crawling schema: <url>:<html>
        self.visited = set([]) # Set of visited URLs for traversal
        self.error_list = [] # List of URLs that were not parse-able
        self.htmlParser = HTMLParser()

    async def run(self, path: str) -> Dict[str, str]:
        """Start URL crawling given file path to a list of urls"""

        with open(path) as file:

            url = file.readline()
            # Read list of files from txt document
            while url:
                print(f"url: {url}")
                task = asyncio.create_task(self.crawlUrl(url.rstrip(), 1))
                url = file.readline()
            
            await task
        
        return self.papers

    async def crawlUrl(self, url: str, counter: int) -> None:
        if url in self.visited:
            return
        
        async with httpx.AsyncClient() as client:
            self.visited.add(url)
            print(f"crawlUrl: {url} counter: {counter}")
            response = await client.get(url)
            responseHtml = response.text
            isPaper, url_list, error_list = self.htmlParser.run(url, responseHtml)

            self.error_list.append(error_list)

            if isPaper:
                self.papers[url] = responseHtml
            
            if counter <= 0:
                return

            for url in url_list:
                task = asyncio.create_task(self.crawlUrl(url, counter - 1))
            
            await task
