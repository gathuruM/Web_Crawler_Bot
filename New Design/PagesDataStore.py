# An abstraction within the crawler that works with MOngo DB
from page import Page
import pymongo
import redis

class LinksDataStore(object):

    def __init__(self, url, signature):
        self.db = self.boot()
        self.url = url
        self.signature = signature
        self.r = redis.Redis(host="localhost", port=5040, db=0)
        pass

    def boot():
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        db = client.LinkStore

        col1 = db["links_to_crawl"]
        col2 = db["crawled_links"]

        return db

    def add_link_to_crawl(self, urls, priority):
        """Add the given link to `links_to_crawl`."""
        for url in urls:
            if (url in self.db.links_to_crawl):
                continue
            if (url in self.db.crawled_links):
                continue
            self.db.links_to_crawl.insert_one
            ( 
                {"url": urls} 
            )
            self.r.zadd("links_to_crawl", {url, priority})  
        pass
    
    # Remove a visited link from links_to_crawl
    def remove_link_to_crawl(self, url, priority):
        """Remove the given link from `links_to_crawl`."""
        self.db.links_to_crawl.delete_one
        (
            {"url": url}
        )
        self.r.zrem("links_to_crawl", {url, priority})
        pass

    # Reduce link priority for a similar link
    def reduce_priority_link_to_crawl(self, url):
        """Reduce the priority of a link in `links_to_crawl` to avoid cycles."""
        self.r.zincrby("links_to_crawl", -1, url)
        
        pass

    def extract_max_priority_page(self):
        """Return the highest priority link in `links_to_crawl`."""
        next_url = self.r.zrange("links_to_crawl", 0, 0)[0]

        return next_url

    # Store the signature and the crawled link in a database
    def insert_crawled_link(self, url, signature):
        """Add the given link to `crawled_links`."""
        
        self.db.crawled_links.insert_one({
            "url": url,
            "signature": signature
        })
        pass

    def crawled_similar(self, url, signature, db):
        """Determine if we've already crawled a page matching the given signature"""
        # Check if the page with the given signature has already been crawled
        # return signature in db
        if not self.crawled_similar(url, signature, db):
        # The page has not been crawled yet, so we can process it
            self.insert_crawled_link(url, signature)
    # ...

