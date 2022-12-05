from catalog import db
from fastapi import FastAPI

app = FastAPI()


@app.get("/search/{term}")
def search(term: str):
    collection = getattr(db.get(), "catalog_items")
    result = collection.find(
        {"$text": {"$search": term}}, projection={"_id": False, "version": False}
    ).sort("score", {"$meta": "textScore"})
    return list(result)
