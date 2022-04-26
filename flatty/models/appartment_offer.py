from typing import Optional

from flatty.models.price import Price

__all__ = ["AppartmentOffer"]


class AppartmentOffer:
    def __init__(
        self,
        name: str,
        area: float,
        floor: str,
        number_of_rooms: int,
        city: str,
        url: str,
        offer_id: str,
        prices_history: "list[Price]",
        id: Optional[str] = None,
    ):
        self.name = name
        self.area = area
        self.floor = floor
        self.number_of_rooms = number_of_rooms
        self.city = city
        self.url = url
        self.offer_id = offer_id
        self.prices_history = prices_history
        self.id = id

    def __str__(self):
        return (
            f"{self.name} [{self.city}] | "
            f"{self.prices_history[0].value} PLN | "
            f"area {self.area} m2"
        )
