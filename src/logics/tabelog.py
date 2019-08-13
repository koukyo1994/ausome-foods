import urllib.parse
import urllib.error

import bs4

import numpy.random as random

import constants as C
import utils as U

from typing import List, Tuple, Dict


def _get_total_page_num(soup: bs4.BeautifulSoup) -> int:
    page_count_num_tags: List[bs4.element.Tag] = soup.findAll(
        "span", attrs={"class": "c-page-count__num"})
    if page_count_num_tags:
        page_count_num = int(page_count_num_tags[-1].text)
        if page_count_num % C.N_RST_IN_PAGE_TABELOG == 0:
            n_total_pages = page_count_num // C.N_RST_IN_PAGE_TABELOG
        else:
            n_total_pages = page_count_num // C.N_RST_IN_PAGE_TABELOG + 1
        return n_total_pages
    else:
        return 0


def _random_choice_rst(soup: bs4.BeautifulSoup) -> Tuple[str, str]:
    rst_tags = soup.find_all("a", attrs={"class": "list-rst__rst-name-target"})
    n_rsts = len(rst_tags)

    rst = rst_tags[random.choice(n_rsts)]
    url = rst.get("href")
    name = rst.text
    return url, name


def _random_choice_img(soup: bs4.BeautifulSoup) -> Tuple[str, str]:
    img_tags = soup.find_all("img", attrs={"class": "rstdtl-photo-list__img"})
    n_imgs = len(img_tags)

    img = img_tags[random.choice(n_imgs)]
    url = img.get("src")
    text = img.get("title")
    return url, text


def tabelog(url: str) -> Dict[str, str]:
    result_dict: Dict[str, str] = {}

    soup = U.fetch_url(url)
    n_rst_pages = _get_total_page_num(soup)
    page_number = random.choice(n_rst_pages) + 1

    soup = U.fetch_one_page(url, page_number)
    for _ in range(C.MAX_RETRY):
        try:
            rst_url, name = _random_choice_rst(soup)
            result_dict["rst_url"] = rst_url
            rst_url = urllib.parse.urljoin(rst_url,
                                           C.PHOTO_SUBDIR_TABELOG) + "/"
            result_dict["rst_name"] = name

            img_soup = U.fetch_one_page(rst_url, 1)
            n_img_pages = _get_total_page_num(img_soup)
            page_number = random.choice(n_img_pages) + 1

            img_page_url = rst_url + "1/smp0/D-normal/" + str(page_number)
            img_soup = U.fetch_url(img_page_url)
            img_url, title = _random_choice_img(img_soup)
            break
        except urllib.error.HTTPError:
            continue
    result_dict["img_name"] = title
    result_dict["img_url"] = img_url
    return result_dict
