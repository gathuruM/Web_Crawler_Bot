from urllib.request import urlopen  # Allows connecting to webpages
from linkFinder import LinkFinder
from general import *
from domain import *
import redis, requests
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
    queue_file = ""
    crawled_file = ""
    r = redis.Redis(host="localhost", port=6040, db=0)
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name) -> None:
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + "/queue.txt"
        Spider.crawled_file = Spider.project_name + "/crawled.txt"
        self.boot()     # make directory
        self.crawl_page("First Spider", Spider.base_url)       # First spider crawls first link

    @staticmethod 
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + " now crawling ->  " + page_url + "\n")
            print("Queue: " + str(len(Spider.queue)) + " | Crawled: " + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

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

        return finder.page_links()
    @staticmethod
    def determine_link_priority(url):
        soup = BeautifulSoup()
        priority = 0
        # Get the contents of the link
        response = requests.get(url)
        content = response.content

        # Parse the HTML content
        soup = BeautifulSoup(content, "html.parser")

        # Check the number of incoming links
        priority += len(soup.find_all("a"))

        # Check for keywords in the title and body
        title = soup.find("title").get_text()
        body = soup.find("body").get_text()
        keywords = ["news", "current events", "breaking"]
        for word in keywords:
            if word in title or word in body:
                priority += 1

        # Check for social media engagement
        socials = ["facebook", "twitter", "instagram"]
        social_tags = soup.find_all(socials)

        priority += len(social_tags)

        return priority

    @staticmethod
    def add_links_to_crawl(links, priority):
        r = redis.Redis()
        for url in links:
            if (url in links.queue):
                continue
            if (url in links.crawled):
                continue
            if (Spider.domain_name not in url):
                continue
            Spider.r.zadd("front queue", {url, priority})

    def extract_max_priority_page(self):
        """Return the highest priority link in `links_to_crawl`."""


    # Reduce priority of similar page in crawled_links
    def reduce_priority(url, signature):
        r = redis.Redis()
        # check for similarity in crawled_links
        r.zincrby("links", -1, url)

    
    def insert_crawled_link(self, url, signature):
        """Add the given link and its signature to `crawled_links` in the database."""
        
        

    def crawled_similar(self, signature):
        """Determine if we've already crawled a page matching the given signature""" 


    # Remove visited link from links_to_crawl in the database
    def remove_link_to_crawl(url, priority):
        r = redis.Redis()
        next_link = r.zrange("links", 0, 0)[0]
        r.zrem("links", next_link)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)