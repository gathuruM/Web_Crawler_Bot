import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = "Techsavanna"
HOMEPAGE = "https://techsavanna.technology"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
NUMBER_OF_THREADS = 8

thread_queue = Queue()      # Threads can only work with queues

# Call the first spider before multi-threading
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Creating worker threads(will die when main exists)
def create_signature(self):
        # Create signature based on url and contents using hashlib
        import hashlib
        import requests

        response = requests.get(self.url)
        content = response.content

        self.signature = hashlib.sha256(content).hexdigest()

        # Store the signature and the crawled link in a database
        self.db.crawled_links.insert_one({
            "url": self.url,
            "signature": self.signature
        })
        pass
    
def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = thread_queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        thread_queue.task_done()

# Check if there are items in the queue if so crawl them
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + " links in the queue")
        create_jobs()       # Only called as long as there are links to be crawled

#  Each queued links is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        thread_queue.put(link)
    thread_queue.join()
    crawl()

create_threads()
crawl()

