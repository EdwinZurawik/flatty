__all__ = ["BaseSerializer"]


class BaseSerializer:
    serialize_schema = None
    deserialize_schema = None

    @classmethod
    def serialize(cls, element_to_serialize: any) -> any:
        return cls.serialize_schema.dump(element_to_serialize)

    @classmethod
    def deserialize(cls, element_to_deserialize: any) -> any:
        return cls.deserialize_schema.load(element_to_deserialize)
