from marshmallow import (
    Schema,
    fields,
    post_load,
)

from flatty.models.appartment_offer import AppartmentOffer
from flatty.schemas.custom_fields import ObjectId
from flatty.schemas.price import PriceSchema

__all__ = ["AppartmentOfferSchema"]


class AppartmentOfferSchema(Schema):
    __model__ = AppartmentOffer
    name = fields.String()
    area = fields.Float()
    floor = fields.String()
    number_of_rooms = fields.Integer()
    city = fields.String()
    url = fields.String()
    offer_id = fields.String()
    has_balcony = fields.Boolean()
    website = fields.String()
    prices_history = fields.List(fields.Nested(PriceSchema))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    id = ObjectId(allow_none=True, data_key="_id")

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)
