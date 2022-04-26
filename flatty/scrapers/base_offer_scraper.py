import requests
from bs4 import BeautifulSoup

from flatty.utils import get_request_headers

__all__ = ["BaseOfferScraper"]


class BaseOfferScraper:
    def __init__(self):
        pass

    def scrape_offers(self):
        return NotImplemented

    def get_page_soup(self, page_url: str) -> BeautifulSoup:
        response = requests.get(page_url, headers=get_request_headers())

        soup = BeautifulSoup(response.text, "html.parser")
        return soup
