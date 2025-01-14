import logging

import scrapy
from bs4 import BeautifulSoup

from ..items import DeepmindPublicationItem

logging.basicConfig(
    filename="logs.txt",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class DeepMindSpider(scrapy.Spider):
    name = "deepmind"
    allowed_domains = ["deepmind.google"]
    start_urls = [
        "https://deepmind.google/research/publications/"
    ]  # main listings page

    def parse(self, response):
        """
        Parses the main listing page for publications and follows links to detail pages.
        Args:
            response (scrapy.http.Response): The response object containing the HTML of the main listing page.
        Yields:
            scrapy.Request: A request to the publication detail page with metadata including the title and URL.
        The function performs the following steps:
        1. Selects all publication elements from the main listing.
        2. Extracts the relative link and title for each publication.
        3. Constructs the full URL for the publication detail page.
        4. Yields a request to the publication detail page, passing along the title and URL as metadata.
        5. Checks for a pagination link to the next page and follows it if present.
        """
        logging.info(f"Parsing URL: {response.url}")

        if not response:
            logging.error("Failed to retrieve the response")

        # For each publication in the main listing
        # Publication is in: <li class="list-compact__item">
        publications = response.css("li.list-compact__item")

        for pub in publications:
            # The link to the detail page is in <a class="list-compact__link--publication">
            rel_link = pub.css("a.list-compact__link--publication::attr(href)").get()
            title = pub.css(
                "a.list-compact__link--publication span.list-compact__inner::text"
            ).get()

            # e.g. rel_link = "/research/publications/101479/"
            # Combine with the domain: "https://deepmind.google" + rel_link
            full_link = response.urljoin(rel_link)

            yield scrapy.Request(
                full_link,
                callback=self.parse_publication,
                meta={"title": title, "pub_url": full_link},  # pass along data
            )

        # If there's pagination (like "?page=2"), follow that too
        next_page = response.css(
            "a.gdm-pagination__trigger.gdm-pagination__trigger--next::attr(href)"
        ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_publication(self, response):
        """
        Parse the publication details from the response.
        This method extracts the title, URL, and abstract of a publication from the response object.
        The abstract is identified by locating the <h2> tag with the text "Abstract" and then
        extracting the text from the subsequent <p> tag.
        Args:
            response (scrapy.http.Response): The response object containing the HTML of the publication page.
        Yields:
            DeepmindPublicationItem: An item containing the title, abstract, and URL of the publication.
        """

        title = response.meta["title"]
        pub_url = response.meta["pub_url"]

        # The HTML structure shows the abstract is in:
        #   <h2>Abstract</h2>
        #   <p> ... </p>

        soup = BeautifulSoup(response.text, "html.parser")

        # Look for <h2> that has text "Abstract", then the next <p> is the abstract
        abstract = "No abstract found"
        abstract_heading = soup.find("h2", string="Abstract")
        if abstract_heading:
            # Typically the abstract is in the next <p> sibling
            next_p = abstract_heading.find_next_sibling("p")
            if next_p:
                abstract = next_p.get_text(strip=True)

        # Build our final item
        item = DeepmindPublicationItem()
        item["title"] = title.strip() if title else "No Title"
        item["abstract"] = abstract
        item["url"] = pub_url  # The detail-page URL on the DeepMind site

        logging.info(f"Scraped item: {item}")

        yield item
