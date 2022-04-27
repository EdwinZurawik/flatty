from marshmallow import (
    Schema,
    fields,
    post_load,
)

from flatty.models.price import Price

__all__ = ["PriceSchema"]


class PriceSchema(Schema):
    __model__ = Price
    created_at = fields.DateTime()
    value = fields.Float()
    currency = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)
