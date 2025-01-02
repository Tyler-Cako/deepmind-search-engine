from html.parser import HTMLParser
from urllib.request import urlopen
from typing import List
from .util import appendUrl, cleanUrl, getRootUrl

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        """Handle <a> tags to continue crawling"""
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    new_url = appendUrl(self.root_url, value) #Make relative url absolute
                    formatted_url = cleanUrl(new_url)
                    self.url_list.append(formatted_url)

    def parse(self, url: str) -> List[str]:
        """Parse a given URL's page. Returns list of links to crawl next"""

        self.url_list = []
        self.root_url = getRootUrl(url)
        self.error_urls = []

        print(self.root_url)

        try:
            print("Enter HTMLParser: run")
            # urlopen returns served html as a bytearray when read, need to decode
            response = urlopen(url)

            # First check if charset is utf8
            content_charset = response.headers.get_content_charset()

            if content_charset != "utf-8":
                raise Exception("HTMLParser parse error. Page not in utf8 encoding!")

            responseHtml = response.read().decode('utf8')
            if responseHtml:
                print("Page received.")
                self.feed(responseHtml)
        except Exception as e:
            print(f"Parsing error from url({url}): {e}")

        return self.url_list, self.error_urls

