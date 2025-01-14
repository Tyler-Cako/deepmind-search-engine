import sqlite3


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
        self.cursor.execute(
            """
            INSERT INTO publications (title, abstract, url)
            VALUES (?, ?, ?)
        """,
            (item["title"], item["abstract"], item["url"]),
        )
        self.connection.commit()
        return item
