import logging
import sqlite3

import pyterrier as pt
from bs4 import BeautifulSoup  # To clean the html

if not pt.started():
    pt.init()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("PyTerrier has started")


def extract_text(html_content):
    """
    Extracts and returns the text content from the given HTML content.

    Args:
        html_content (str): A string containing HTML content.

    Returns:
        str: The extracted text content from the HTML.
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text()
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return ""


try:
    # TODO - Connect to database with appropriate path
    conn = sqlite3.connect("")  # Path to database
    logger.info("Connected to database")
    c = conn.cursor()

    # Fetch documents
    c.execute("SELECT id, html_content FROM webpages")
    documents = []
    for doc_id, html in c.fetchall():
        documents.append({"docno": doc_id, "text": extract_text(html)})

    logger.info(f"Indexing {len(documents)} documents")

    # Index documents
    indexer = pt.IterDictIndexer("../index", meta={"docno": 20, "text": 4096})
    index_ref = indexer.index(documents)
    logger.info("Indexing completed successfully")
    index = pt.IndexFactory.of(index_ref)
    bm25 = pt.BatchRetrieve(index, wmodel="BM25")

except sqlite3.Error as e:
    logger.error(f"Database error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
finally:
    if conn:
        conn.close()
        logger.info("Database connection closed")
