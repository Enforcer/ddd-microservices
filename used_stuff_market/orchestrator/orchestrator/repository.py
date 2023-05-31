import json
from typing import ClassVar

from orchestrator import db
from orchestrator.process_manager import AddingNewItemProcessManager
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


class AddingNewItemProcessManagerRepository:
    COLLECTION_NAME: ClassVar = "process_manager_adding_new_item"

    class NotFound(Exception):
        pass

    class AlreadyExists(Exception):
        pass

    def insert(self, pm: AddingNewItemProcessManager) -> None:
        as_json = json.loads(pm.json())
        try:
            self._collection().insert_one(as_json)
        except DuplicateKeyError:
            raise self.AlreadyExists

    def update(self, pm: AddingNewItemProcessManager) -> None:
        as_json = json.loads(pm.json())
        filter_cond = {
            "item_id": pm.item_id,
        }
        result = self._collection().replace_one(
            filter=filter_cond,
            replacement=as_json,
        )
        if result.matched_count != 1:
            raise self.NotFound

    def get(self, item_id: int) -> AddingNewItemProcessManager:
        filter_cond = {
            "item_id": item_id,
        }
        if raw := self._collection().find_one(filter_cond):
            del raw["_id"]
            return AddingNewItemProcessManager(**raw)
        else:
            raise self.NotFound

    def _collection(self) -> Collection:
        return getattr(db.get(), self.COLLECTION_NAME)
