import re
import time
from datetime import datetime

from bs4 import BeautifulSoup
from flatty.models.appartment_offer import AppartmentOffer
from flatty.scrapers.base_offer_scraper import BaseOfferScraper
from flatty.serializers.appartment_offer_serializer import AppartmentOfferSerializer

__all__ = ["NieruchomosciOnlineScraper"]


class NieruchomosciOnlineScraper(BaseOfferScraper):
    def scrape_offers(self, city: str) -> "list[AppartmentOffer]":
        url = (
            "https://www.nieruchomosci-online.pl/szukaj.html?"
            f"3,mieszkanie,sprzedaz,,{city}"
        )
        links = self.get_offer_links_from_page(self.get_page_soup(url))

        data = []
        for link in links:
            time.sleep(2)
            if len(data) >= 3:
                break
            base_data = {
                "city": city,
                "url": link,
            }
            offer_data = self.get_offer_data(self.get_page_soup(link))
            if offer_data:
                print(f"Collected data for {offer_data['name']}...")
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
            "#attributesTable div:nth-of-type(2) " "span:nth-of-type(2)"
        )
        floor = soup.select("#attributesTable div:first-of-type " "span:nth-of-type(2)")
        name = soup.find(class_="h1Title")
        offer_id = soup.select("input[name='idData']")
        data_list = [area, price, number_of_rooms, name, floor]

        if not all(data_list):
            print(f"{name.text} - data missing...")
            return None
        area = self.clean_number_data(area.text)
        price = self.clean_number_data(price.text)
        number_of_rooms = self.clean_number_data(number_of_rooms[0].text)

        data = {
            "area": area,
            "prices_history": [
                {"created_at": datetime.now().isoformat(), "value": price}
            ],
            "number_of_rooms": int(number_of_rooms),
            "name": name.text,
            "floor": floor[0].text,
            "offer_id": offer_id[0].get("value"),
        }
        return data

    def clean_number_data(self, number: str) -> float:
        number = re.sub(r"\xa0", "", number)
        number = re.sub(r",", ".", number)
        number_regex = re.compile(r"[0-9.]*")
        match_data = number_regex.match(number)
        if match_data:
            return float(match_data.group())
        raise ValueError(
            f"Incorrect value. Expected {type(str)}, but got"
            f"{type(match_data)} instead!"
        )


# TODO:
# dodać id (do znalezienia w urlu)
# https://www.nieruchomosci-online.pl/mieszkanie,m2,z-oddzielna-kuchnia/23303650.html?i
# dodać pozostałe dane i ujednolicić z modelem
# rozbić scrapowanie na moduły
