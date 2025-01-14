import scrapy
from bs4 import BeautifulSoup
from ..items import DeepmindPublicationItem

# TODO Complete the AppleMLSpider class
class AppleMLSpider(scrapy.Spider):
    name = "appleml"
    allowed_domains = ["machinelearning.apple.com"]
    start_urls = ["https://machinelearning.apple.com/research"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("div", class_="research-entry")

        for article in articles:
            title_tag = article.find("h3")
            abstract_tag = article.find(
                "p"
            ) 

            item = DeepmindPublicationItem()
            item["title"] = title_tag.get_text(strip=True) if title_tag else "No Title"
            item["abstract"] = (
                abstract_tag.get_text(strip=True) if abstract_tag else "No Abstract"
            )

            yield item
