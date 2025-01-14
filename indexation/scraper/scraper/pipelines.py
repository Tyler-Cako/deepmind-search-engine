# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("deepmind_publications.db")
        self.cursor = self.connection.cursor()
        # Create table if not exists
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                abstract TEXT,
                url TEXT
            )
        """
        )
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cursor.execute(
            """
            INSERT INTO publications (title, abstract, url)
            VALUES (?, ?, ?)
        """,
            (adapter.get("title"), adapter.get("abstract"), adapter.get("url")),
        )
        self.connection.commit()
        return item
