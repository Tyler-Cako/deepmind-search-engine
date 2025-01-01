from urllib import request, robotparser
from urllib.parse import urlparse
from .parser.parser import HTMLParser

class Crawler(object):
    """Crawler object with various methods to crawl the web based on document of seed URLs."""

    def __init__(self):
        self.to_visit = []
        self.visited = set()
        self.pasrer = HTMLParser()
        self.robotParser = robotparser.RobotFileParser()

    def canCrawl(self, url:str) -> True:
        """Check Robots.txt to see if we can crawl this URL"""

        return self.robotParser.can_fetch("*", url)
        # root_url = urlparse(url).hostname
        # robot_url = root_url + "/robots.txt"
        # self.robotParser.set_url(robot_url)
    
    def crawl(self, path: str) -> None:
        """Start URL crawling given file path to a list of urls"""
        
        file = open(path)
        
        url = file.readline()
        # Read list of files from txt document
        while url:
            print(f"url: {url}")
            self.crawlUrl(url, 10)
            url = file.readline()
        
        file.close()

    def crawlUrl(self, url: str, counter: int) -> None:
        """Crawl a specific URL. Counter designates max depth of search"""

        if url in self.visited:
            return
        
        #Check robots.txt
        if not self.canCrawl(url):
            return
        
        #Parse URL
        url_list = [] # New URLs to crawl 

        self.visited.add(url)

        if counter > 0:
            for url in url_list:
                self.crawlUrl(url, counter - 1)