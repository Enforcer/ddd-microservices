import json
from typing import ClassVar

from negotiations.application.repository import NegotiationsRepository
from negotiations.domain.negotiation import Negotiation
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError


class MongoDbNegotiationsRepository(NegotiationsRepository):
    COLLECTION_NAME: ClassVar = "negotiations"

    def __init__(self, database: Database) -> None:
        self._db = database

    def insert(self, negotiation: Negotiation) -> None:
        as_json = json.loads(negotiation.json())
        try:
            self._collection().insert_one(as_json)
        except DuplicateKeyError:
            raise self.AlreadyExists

    def update(self, negotiation: Negotiation) -> None:
        as_json = json.loads(negotiation.json())
        filter_cond = {
            "item_id": negotiation.item_id,
            "buyer_id": negotiation.buyer_id,
            "seller_id": negotiation.seller_id,
        }
        result = self._collection().replace_one(
            filter=filter_cond,
            replacement=as_json,
        )
        if result.matched_count != 1:
            raise self.NotFound

    def get(self, item_id: int, buyer_id: int, seller_id: int) -> Negotiation:
        filter_cond = {
            "item_id": item_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
        }
        if raw := self._collection().find_one(filter_cond):
            del raw["_id"]
            return Negotiation(**raw)
        else:
            raise self.NotFound

    def _collection(self) -> Collection:
        return getattr(self._db, self.COLLECTION_NAME)
