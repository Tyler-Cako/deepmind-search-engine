from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.request import urlopen
from typing import List, Tuple, Generator
from .util import cleanUrl, getHostName, isValid, isPaper
import re

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        """Handle <a> tags to continue crawling"""
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    new_url = urljoin(self.url, value) #Make relative url absolute
                    formatted_url = cleanUrl(new_url)

                    if isValid(formatted_url, self.hostname):
                        self.url_list.append(formatted_url)

    def run(self, url: str) -> Tuple[List[str], List[str], List[str]]:
        """Parse a given URL's page. Returns list of links to crawl next"""

        self.hostname = getHostName(url)
        self.url = url
        self.url_list = []
        self.error_list = []

        try:
            print(f"HTMLParser.parse: url: {url}")
            html = ""
            # urlopen returns served html as a bytearray when read, need to decode
            response = urlopen(url)

            # First check if charset is utf8
            content_charset = response.headers.get_content_charset()

            if content_charset != "utf-8":
                raise Exception("HTMLParser parse error. Page not in utf8 encoding!")

            responseHtml = response.read().decode('utf8')
            if responseHtml:
                self.feed(responseHtml)

                if isPaper(url):
                    print(f"paper found! Adding ({url})")
                    html = responseHtml

        except Exception as e:
            print(f"Parsing error from url({url}): {e}")
            self.error_list.append(url)

        return html, self.url_list, self.error_list