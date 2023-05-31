import logging
from uuid import UUID

from pydantic import BaseModel

import mqlib
from orchestrator.queues import register_resource, add_catalog_item


class ItemCdcData(BaseModel):
    item_id: int
    title: str
    description: str
    price: dict[str, str]
    version: int


class ItemAddedData(BaseModel):
    item_id: int
    owner_id: int


class AddingNewItemProcessManager(BaseModel):
    item_id: int

    cdc_data: ItemCdcData | None = None
    item_added_data: ItemAddedData | None = None
    item_registered: bool = False

    def item_changed(self, cdc_data: ItemCdcData) -> None:
        self.cdc_data = cdc_data
        self._on_data_changed()

    def item_added(self, item_added_data: ItemAddedData) -> None:
        self.item_added_data = item_added_data
        self._on_data_changed()

    def resource_registered(self) -> None:
        self.item_registered = True
        self._on_data_changed()

    def _on_data_changed(self) -> None:
        if self._data_complete_but_not_registered():
            logging.info("Data complete, not registered, registering...")
            mqlib.publish(register_resource, message={
                "resource_id": self.item_id,
                "owner_id": str(UUID(int=self.item_added_data.owner_id)),
            })
        elif self._data_complete_and_registered():
            logging.info("Data complete and registered, adding to catalog")
            mqlib.publish(add_catalog_item, message=self.cdc_data.dict())
        else:
            logging.info("Data not complete yet, not doing anything")

    def _data_complete_but_not_registered(self):
        return (
            self.cdc_data is not None
            and self.item_added_data is not None
            and not self.item_registered
        )

    def _data_complete_and_registered(self):
        return (
            self.cdc_data is not None
            and self.item_added_data is not None
            and self.item_registered
        )