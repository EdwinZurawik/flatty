from datetime import datetime

__all__ = ["Price"]


class Price:
    def __init__(
        self, value: float, created_at: datetime = None, currency: str = "PLN"
    ):
        self.created_at = created_at if created_at else datetime.now()
        self.value = value
        self.currency = currency

    def __str__(self):
        return f"{self.created_at}: {self.value} {self.currency}"
