import json
import time
import urllib.request
import urllib.parse

import numpy.random as random

import constants as C

from typing import Tuple

from bs4 import BeautifulSoup


def url_select() -> Tuple[str, str]:
    with open(C.URL_FILE) as f:
        urls = json.load(f)

    key = random.choice(list(urls.keys()))
    return key, urls[key]


def fetch_url(url: str) -> BeautifulSoup:
    html = urllib.request.urlopen(url)
    time.sleep(1)
    soup = BeautifulSoup(html, "html.parser")
    return soup


def fetch_one_page(url: str, page: int) -> BeautifulSoup:
    html = urllib.request.urlopen(urllib.parse.urljoin(url, str(page)))
    time.sleep(1)
    soup = BeautifulSoup(html, "html.parser")
    return soup


if __name__ == '__main__':
    print(url_select())
    key, url = url_select()
    soup = fetch_url(url)
    import ipdb
    ipdb.set_trace()
    print(type(fetch_url(url)))
