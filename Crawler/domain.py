from urllib.parse import urlparse

# Get the domain name(example.com)
def get_domain_name(url):
    try:
        result = get_subdomain_name(url).split('.')
        return ".".join(result[-2:])
    except:
        return ""


# Get the sub domain name(name.example.com)
def get_subdomain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ""

