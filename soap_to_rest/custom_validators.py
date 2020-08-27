from urllib.parse import urlparse


def is_web_url(possible_url):
    parsed_url = urlparse(possible_url)
    if parsed_url.scheme not in ["http", "https"]:
        raise ValueError()
