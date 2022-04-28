import re
import time

from bs4 import BeautifulSoup

from flatty.models.appartment_offer import AppartmentOffer
from flatty.scrapers.base_offer_scraper import BaseOfferScraper
from flatty.serializers.appartment_offer_serializer import AppartmentOfferSerializer

__all__ = ["NieruchomosciOnlineScraper"]


class NieruchomosciOnlineScraper(BaseOfferScraper):
    def __init__(self):
        super().__init__()
        self.website = "Nieruchomości Online"

    def scrape_offers(self, city: str) -> "list[AppartmentOffer]":
        page_empty = False
        page_number = 1
        offers = []
        while not page_empty:
            url = (
                "https://www.nieruchomosci-online.pl/szukaj.html?"
                f"3,mieszkanie,sprzedaz,,{city}&p={page_number}"
            )
            offer_links = self.get_offer_links_from_page(self.get_page_soup(url))
            if not offer_links:
                page_empty = True
                print(f"Page {page_number} is empty. Stopping...")
                continue
            print(f"Getting offers from page {page_number}...")
            offers_from_page = self.scrape_offers_from_page(offer_links, city)
            offers.extend(offers_from_page)
            page_number += 1
        return offers

    def scrape_offers_from_page(
        self, links: "list[str]", city: str
    ) -> "list[AppartmentOffer]":
        data = []
        offers = []
        for link in links:
            time.sleep(1)
            base_data = {
                "city": city,
                "url": link,
                "website": self.website,
            }
            offer_data = self.get_offer_data(self.get_page_soup(link))
            if offer_data:
                # print(f"Collected data for {offer_data['name']}...")
                data.append({**offer_data, **base_data})

        offers = [
            AppartmentOfferSerializer.deserialize(appartment_data)
            for appartment_data in data
        ]
        return offers

    def get_offer_links_from_page(self, soup: BeautifulSoup) -> "list[str]":
        return [link.get("href") for link in soup.select(".name a")]

    def get_offer_data(self, soup: BeautifulSoup) -> "dict[any, any]":
        area = soup.find(class_="info-area")
        price = soup.find(class_="info-primary-price")
        number_of_rooms = soup.select(
            "#attributesTable div:nth-of-type(2) span:nth-of-type(2)"
        )
        floor = soup.select("#attributesTable div:first-of-type span:nth-of-type(2)")
        name = soup.find(class_="h1Title")
        offer_id = soup.select("#bottomForm input[name='idData']")
        has_balcony = self.check_if_has_balcony(soup)
        data_list = [area, price, number_of_rooms, name, floor]

        if not all(data_list):
            # print(f"{name.text} - data missing...")
            return None
        try:
            area = self.clean_number_data(area.text)
            price = self.clean_number_data(price.text)
            number_of_rooms = self.clean_number_data(number_of_rooms[0].text)
        except ValueError as e:
            print(f"Error: {e}")
            return None

        data = {
            "area": area,
            "prices_history": [{"value": price}],
            "number_of_rooms": int(number_of_rooms),
            "name": name.text,
            "floor": floor[0].text,
            "offer_id": offer_id[0].get("value"),
            "has_balcony": has_balcony,
        }
        return data

    def check_if_has_balcony(self, soup: BeautifulSoup):
        additional_area = soup.find_all("strong", text="Powierzchnia dodatkowa:")
        if additional_area:
            additional_area_text = additional_area[0].findNext("span").text
            return any([word in additional_area_text for word in ("balkon", "loggia")])
        return False

    def clean_number_data(self, number: str) -> float:
        number = re.sub(r"\xa0", "", number)
        number = re.sub(r",", ".", number)
        number_regex = re.compile(r"[0-9.]+")
        match_data = number_regex.match(number)
        if match_data:
            return float(match_data.group())
        print(number, match_data)
        raise ValueError(
            f"Incorrect value. Expected {type(str)}, but got"
            f"{type(match_data)} instead!"
        )


# TODO:
# dodać id (do znalezienia w urlu)
# https://www.nieruchomosci-online.pl/mieszkanie,m2,z-oddzielna-kuchnia/23303650.html?i
# dodać pozostałe dane i ujednolicić z modelem
# rozbić scrapowanie na moduły
