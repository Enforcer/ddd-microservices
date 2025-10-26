from catalog import db, dao
from fastapi import FastAPI

app = FastAPI()


@app.get("/search/{term}")
def search(term: str):
    collection = getattr(db.get(), "catalog_items")
    result = collection.find(
        {"$text": {"$search": term}}, projection={"_id": False, "version": False}
    ).sort("score", {"$meta": "textScore"})
    return list(result)


@app.post("/items")
def register_item(data: dict) -> None:
    data["likes"] = 0
    dao.upsert(item_id=data["item_id"], data=data)
