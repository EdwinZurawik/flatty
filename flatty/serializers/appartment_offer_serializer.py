from flatty.schemas.appartment_offer import AppartmentOfferSchema
from flatty.serializers.base_serializer import BaseSerializer

__all__ = ["AppartmentOfferSerializer"]


class AppartmentOfferSerializer(BaseSerializer):
    serialize_schema = AppartmentOfferSchema(exclude=["id"])
    deserialize_schema = AppartmentOfferSchema()
