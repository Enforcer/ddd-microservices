import random
from collections import defaultdict

from catalog import db, dao
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/search/{term}")
def search(term: str):
    collection = getattr(db.get(), "catalog_items")
    result = collection.find(
        {"$text": {"$search": term}}, projection={"_id": False, "version": False}
    ).sort("score", {"$meta": "textScore"})
    return list(result)


errors_left_by_item_id: dict[int, int] = {}


@app.post("/items")
def register_item(data: dict) -> Response:
    item_id = data["item_id"]
    if item_id not in errors_left_by_item_id:
        errors_left_by_item_id[item_id] = random.randint(1, 3)

    if errors_left_by_item_id[item_id] > 0:
        errors_left_by_item_id[item_id] -= 1
        return Response(status_code=500)

    data["likes"] = 0
    dao.upsert(item_id=item_id, data=data)
    return Response()
