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
            self._create_new_offer(offer_serialized)
        else:
            self._update_old_offer(offer_serialized, offer_from_db)

    def _create_new_offer(self, offer_serialized: "dict[str, any]") -> None:
        self._db_manager.save_document(offer_serialized)

    def _update_old_offer(
        self, offer_serialized: "dict[str, any]", offer_from_db: "dict[str, any]"
    ) -> None:
        updated_prices = offer_from_db["prices_history"] + self._get_new_prices(
            offer_serialized["prices_history"], offer_from_db["updated_at"]
        )

        self._db_manager.update_document(
            {"offer_id": offer_serialized["offer_id"]},
            {
                "$set": {
                    "prices_history": updated_prices,
                    "updated_at": offer_serialized["updated_at"],
                }
            },
        )

    def _get_new_prices(self, prices_history: "dict[str, any]", updated_at: str):
        return list(
            filter(lambda price: price["created_at"] > updated_at, prices_history)
        )
