from datetime import datetime

__all__ = ["Price"]


class Price:
    def __init__(self, created_at: datetime, value: float):
        self.created_at = created_at
        self.value = value

    def __str__(self):
        return f"{self.created_at}: {self.value} PLN"
