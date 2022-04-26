from flatty.database.mongodb_manager import DatabaseManager
from flatty.models.appartment_offer import AppartmentOffer
from flatty.serializers.appartment_offer_serializer import AppartmentOfferSerializer

__all__ = ["OfferActualizer"]


class OfferActualizer:
    def __init__(self):
        self._db_manager = DatabaseManager("offers")

    def actualize_offers(self, offers: "list[AppartmentOffer]") -> None:
        print("Actualizing offer...")
        for offer in offers:
            self._actualize_offer(offer)

    def _actualize_offer(self, offer: AppartmentOffer) -> None:
        offer_serialized = AppartmentOfferSerializer.serialize(offer)
        offer_from_db = self._db_manager.get_document(
            {"offer_id": offer_serialized["offer_id"]}
        )
        if offer_from_db is None:
            self._db_manager.save_document(offer_serialized)
        else:
            actual_prices = offer_from_db["prices_history"]
            for price in offer_serialized["prices_history"]:
                if all(
                    actual["created_at"] != price["created_at"]
                    for actual in actual_prices
                ):
                    actual_prices.append(price)
            self._db_manager.update_document(
                {"offer_id": offer_serialized["offer_id"]},
                {"$set": {"prices_history": actual_prices}},
            )
