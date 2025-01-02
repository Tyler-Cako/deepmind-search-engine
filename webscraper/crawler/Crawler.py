from urllib import request, robotparser
from urllib.parse import urlparse
from .parser.parser import HTMLParser

class Crawler(object):
    """Crawler object with various methods to crawl the web based on document of seed URLs."""

    def __init__(self):
        self.to_visit = []
        self.visited = set([])
        self.parser = HTMLParser()
        self.robotParser = robotparser.RobotFileParser()

    def crawl(self, path: str) -> None:
        """Start URL crawling given file path to a list of urls"""

        # file = open(path)
        with open(path) as file:

            url = file.readline()
            # Read list of files from txt document
            while url:
                print(f"url: {url}")
                self.crawlUrl(url, 10)
                url = file.readline()

        # file.close()

    def crawlUrl(self, url: str, counter: int) -> None:
        """Crawl a specific URL. Counter designates max depth of search"""

        if url in self.visited:
            return

        # Check robots.txt
        if not self.canCrawl(url):
            return

        # Parse URL
        url_list = self.parser.parse(url) # New URLs to crawl

        self.visited.add(url)

        if counter > 0:
            for url in url_list:
                print(f"url: {url} \nself.visited: {self.visited}")
                if url not in self.visited:
                    self.crawlUrl(url, counter - 1)

    def canCrawl(self, url: str) -> bool:
        """Check Robots.txt to see if we can crawl this URL"""

        print("enter canCrawl")
        can_fetch = self.robotParser.can_fetch("*", url)
        print(can_fetch)
        return True
        # root_url = urlparse(url).hostname
        # robot_url = root_url + "/robots.txt"
        # self.robotParser.set_url(robot_url)