from html.parser import HTMLParser
from urllib.request import urlopen
from typing import List

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        """Handle <a> tags to continue crawling"""


    def parse(self, url: str) -> List[str]:
        """Parse a given URL's page. Returns list of links to crawl next"""

        print("test")

        self.url_list = []

        try:
            print("Enter HTMLParser: run")
            # urlopen returns served html as a bytearray when read, need to decode
            response = urlopen(url)

            # First check if charset is utf8
            content_charset = response.headers.get_content_charset()

            if content_charset != "utf8":
                raise Exception("HTMLParser parse error. Page not in utf8 encoding!")

            responseHtml = response.read().decode('utf8')
            if responseHtml:
                print("Page received.")
                self.feed(responseHtml)
        except Exception as inst:
            print(f"parsing error: {inst}")


        return self.url_list
