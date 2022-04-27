from datetime import datetime
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
        has_balcony: bool,
        website: str,
        id: Optional[str] = None,
        **kwargs,
    ):
        self.name = name
        self.area = area
        self.floor = floor
        self.number_of_rooms = number_of_rooms
        self.city = city
        self.url = url
        self.offer_id = offer_id
        self.has_balcony = has_balcony
        self.website = website
        self.id = id
        self.prices_history: "list[Price]" = kwargs.get("prices_history", [])
        self.created_at: datetime = kwargs.get("created_at", datetime.now())
        self.updated_at: datetime = kwargs.get("updated_at", datetime.now())

    @property
    def current_price(self) -> Price:
        return self.prices_history[-1]

    def __str__(self):
        return (
            f"{self.name} [{self.city}] | "
            f"{self.prices_history[0].value} PLN | "
            f"area {self.area} m2 | "
            f"ID {self.offer_id}"
        )
