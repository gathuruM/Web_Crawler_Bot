from urllib.request import urlopen  # Allows connecting to webpages
from linkFinder import LinkFinder
from general import *
from domain import *
import redis, requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

    # 1. Spider picks a url from the waiting list, connects to its web page, and sends the HTMl to the Linkfinder class
    #  which then parses through the HTML and returns all the links
    # 2. The Spider also crawls the page and adds unvisited links to the waiting list
    # 3. When it's done crawling it moves the url crawled to the crawled list.

class Spider:

    # Making a class variable, can be shared among all instances(spiders)
    project_name = ""
    base_url = ""
    domain_name = ""
    # queue_file = ""
    # crawled_file = ""
    # r = redis.Redis(host="localhost", port=6040, db=0)
    queue = set()
    crawled = set()
    
    

    def __init__(self, project_name, base_url, domain_name) -> None:
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + "/queue.txt"
        Spider.crawled_file = Spider.project_name + "/crawled.txt"
        Spider.client = MongoClient()
        Spider.db = Spider.client.test_database
        Spider.collection = Spider.db.test_collection
        # self.boot()     # make directory
        self.crawl_page("First Spider", Spider.base_url)       # First spider crawls first link

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + " now crawling ->  " + page_url + "\n")
            print("Queue: " + str(len(Spider.queue)) + " | Crawled: " + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            # Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        # Need to convert the HTML bytes received to readable HTML for the parser 
        html_string = ""
        try:
            response = urlopen(page_url)
            # Confirm if the Content-Type header of the response is equal to "text/html"
            if "text/html" in response.getheader("Content-Type"):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")

            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print("Error crawling this page")
            return set()

        return finder.page_info()

    @staticmethod
    # PRIORITY NOT INCLUDED
    def add_links_to_queue(links):
        # r = redis.Redis()
        for url in links:
            if (url in links.queue):
                continue
            if (url in links.crawled):
                continue
            if (Spider.domain_name not in url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def add_info_to_db(links):
        for url in links:
            Spider.collection.insert_one({'url': url})