from urllib import robotparser
from urllib.request import urlopen
from urllib.parse import urlparse
from .parser.parser import HTMLParser
from typing import Dict

class Crawler(object):
    """Crawler object with various methods to crawl the web based on document of seed URLs."""

    def __init__(self):
        self.to_visit = []
        self.visited = set([])
        self.parser = HTMLParser()
        self.robotParser = robotparser.RobotFileParser()
        self.error_urls = []
        self.papers = {}

    def run(self, path: str) -> Dict[str, str]:
        """Start URL crawling given file path to a list of urls"""

        # file = open(path)
        with open(path) as file:

            url = file.readline()
            # Read list of files from txt document
            while url:
                self.crawlUrl(url, 1)
                url = file.readline()

            if len(self.error_urls) > 1:
                print(f"error urls:")
                for error_url in self.error_urls:
                    print(f"error: {error_url}")

        return self.papers

    def crawlUrl(self, url: str, counter: int) -> None:
        """Crawl a specific URL. Counter designates max depth of search"""

        if url in self.visited:
            return

        # Check robots.txt
        if not self.canCrawl(url):
            return

        # Parse URL
        html, url_list, error_list = self.parser.run(url) # New URLs to crawl

        self.visited.add(url)
        self.error_urls.append(error_list)

        if html:
            self.papers[url] = html


        if counter > 0:
            for url in url_list:
                if url not in self.visited:
                    self.crawlUrl(url, counter - 1)

    def canCrawl(self, url: str) -> bool:
        """Check Robots.txt to see if we can crawl this URL"""

        return True

        self.robotParser.set_url(url)
        self.robotParser.read()

        can_fetch = self.robotParser.can_fetch("*", url)

        return can_fetch
        # root_url = urlparse(url).hostname
        # robot_url = root_url + "/robots.txt"
        # self.robotParser.set_url(robot_url)