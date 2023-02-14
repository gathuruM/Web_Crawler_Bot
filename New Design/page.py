from linkFinder import LinkFinder
class Page(object):

    def __init__(self, url, contents):
        self.url = url
        self.contents = contents
        self.child_urls = LinkFinder.page_links(self)
        self.signature = self.create_signature()

    def create_signature(self):
        # Create signature based on url and contents using hashlib
        import hashlib
        import requests

        response = requests.get(self.url)
        content = response.content

        self.signature = hashlib.sha256(content).hexdigest()

        return self.signature

        