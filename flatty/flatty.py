from dotenv import load_dotenv

from flatty.database import OfferActualizer
from flatty.models import AppartmentOffer
from flatty.scrapers import NieruchomosciOnlineScraper

load_dotenv()


def get_offers_for_city(city: str) -> "list[AppartmentOffer]":
    print(f"Getting offers for {city} city...")
    offers_list = NieruchomosciOnlineScraper().scrape_offers(city)
    print(f"Collected {len(offers_list)} offers for city {city}...")
    return offers_list


def update_offers(offers_list: "list[AppartmentOffer]") -> None:
    OfferActualizer().actualize_offers(offers_list)
    print("Offer actualization completed...")
