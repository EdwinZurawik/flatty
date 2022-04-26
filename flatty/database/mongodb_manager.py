import os

import pymongo
from bson import ObjectId

__all__ = ["DatabaseManager"]


class DatabaseManager:
    def __init__(self, table_name: str) -> None:
        self._uri = os.environ["MONGO_URL"]
        self._table_name = table_name

    def save_document(self, data: "dict[str, any]") -> ObjectId:
        with pymongo.MongoClient(self._uri) as client:
            db = client.get_database()
            id = db[self._table_name].insert_one(data).inserted_id
            return id

    def get_document(self, query: "dict[any, any]") -> "dict[any, any]":
        with pymongo.MongoClient(self._uri) as client:
            db = client.get_database()
            return db[self._table_name].find_one(query)

    def get_documents(self, query: "dict[any, any]") -> "list[dict[any, any]]":
        with pymongo.MongoClient(self._uri) as client:
            db = client.get_database()
            return list(db[self._table_name].find(query))

    def update_document(self, query: "dict[any, any]", data: "dict[any, any]") -> int:
        with pymongo.MongoClient(self._uri) as client:
            db = client.get_database()
            return db[self._table_name].update_one(query, data).modified_count
