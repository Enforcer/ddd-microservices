from pydantic import BaseModel


class AddingNewItemProcessManager(BaseModel):
    item_id: int
