from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

# Input main url
url = "https://techsavanna.technology/"

# Fetch HTML and Convert the HTML bytes received to readable HTML for the parser 
response = urlopen(url)
html_string = ""
try: 
    if "text/html" in response.getheader("Content-Type"):
        html_bytes = response.read()
        html_string = html_bytes.decode("utf-8")

    # Feed the HTML to the finder to extract links and relevant info
except:
    print("Error crawling this page!")
    return set()

# return finder.links()

# Extract links and text -> using new tech for js webpages
    # Spider()
# Log links to the console

# Add links to cache queue and database

# Extract text details to be displayed

# Put text in database


