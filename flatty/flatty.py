from dotenv import load_dotenv

from flatty.database import OfferActualizer
from flatty.scrapers import NieruchomosciOnlineScraper

load_dotenv()


def get_offers_for_city(city: str) -> None:
    print(f"Getting offers for {city} city...")

    offer_actualizer = OfferActualizer()

    scraper = NieruchomosciOnlineScraper()
    data = scraper.scrape_offers("Rybnik")
    print("Found offers:\n")
    for index, offer in enumerate(data):
        print(f"{index + 1}.", offer)

    print("Testing saving documents...")

    offer_actualizer.actualize_offers(data)
