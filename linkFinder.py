# HTMLParser parses through some HTML code
from html.parser import HTMLParser
from urllib import parse 
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import stemmer

class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url) -> None:
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.reverse_index = defaultdict(list)

    # When calling HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_links(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)
        return self.links

    def process_link(self, page_url):
        # Get the contents of the link
        response = requests.get(page_url)
        content = response.content

        # Fetch the contents of the link
        soup = BeautifulSoup(content, "html.parser")

        # Extract the text from the page
        text = soup.get_text()

        # Tokenize the text
        words = text.split()

        # Stem the words
        stemmed_words = [stemmer.stem(word) for word in words]

        for word in stemmed_words:
            self.reverse_index[word].append(page_url)

        return self.reverse_index
    
    def determine_link_priority(url):
         # Parse the HTML content
        soup = BeautifulSoup(contents, "html.parser")
        priority = 0

        # Get the contents of the link
        response = requests.get(url)
        contents = response.content

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
    
    def error(self, message: str):
        # return super().error(message)
        pass

    

    