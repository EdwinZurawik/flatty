import argparse

from dotenv import load_dotenv

from flatty import get_offers_for_city, update_offers

__all__ = ["get_offers_for_city"]

parser = argparse.ArgumentParser()

parser.add_argument("city", help="Select city where appartment should be located")

args = parser.parse_args()

load_dotenv()


def main():
    print("Starting program...")
    offers_list = get_offers_for_city(args.city)
    update_offers(offers_list)


if __name__ == "__main__":
    main()
