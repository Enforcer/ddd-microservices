import json
from typing import ClassVar

from negotiations import db
from negotiations.negotiation import Negotiation
from pymongo.collection import Collection


class NegotiationsRepository:
    COLLECTION_NAME: ClassVar = "negotiations"

    class NotFound(Exception):
        pass

    def save(self, negotiation: Negotiation) -> None:
        as_json = json.loads(negotiation.json())
        filter_cond = {
            "item_id": negotiation.item_id,
            "buyer_id": negotiation.buyer_id,
            "seller_id": negotiation.seller_id,
        }
        self._collection().replace_one(
            filter=filter_cond,
            replacement=as_json,
            upsert=True,
        )

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
        return getattr(db.get(), self.COLLECTION_NAME)
