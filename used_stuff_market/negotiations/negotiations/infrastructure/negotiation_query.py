from typing import ClassVar, Optional

from pymongo.database import Database


class NegotiationQuery:
    COLLECTION_NAME: ClassVar = "negotiations"

    def __init__(self, database: Database) -> None:
        self._db = database

    class RequestedByNonParticipant(Exception):
        pass

    class NotFound(Exception):
        pass

    def run(
        self,
        requesting_party_id: int,
        seller_id: int,
        buyer_id: int,
        item_id: int,
    ) -> dict:
        if requesting_party_id not in (seller_id, buyer_id):
            raise self.RequestedByNonParticipant

        filter_cond = {
            "item_id": item_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
        }
        collection = self._db[self.COLLECTION_NAME]
        document = collection.find_one(filter_cond, projection={"_id": False})

        if document is None or document["broken_off"]:
            raise self.NotFound

        return document
