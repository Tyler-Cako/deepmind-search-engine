import scrapy


class DeepmindPublicationItem(scrapy.Item):
    title = scrapy.Field()
    abstract = scrapy.Field()
    url = scrapy.Field()
