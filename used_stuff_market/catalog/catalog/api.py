from catalog import db
from fastapi import FastAPI

app = FastAPI()


@app.get("/search/{term}")
def search(term: str):
    collection = getattr(db.get(), "catalog_items")
    result = collection.aggregate(
        [
            {"$match": {"$text": {"$search": term}}},
            {
                "$project": {
                    "_id": False,
                    "version": False,
                }
            },
            {
                "$project": {
                    "item_id": True,
                    "title": True,
                    "description": True,
                    "price": True,
                    "likes": {"$size": "$likes"},
                },
            },
            {"$sort": {"$text": {"$meta": "textScore"}}},
        ]
    )
    return list(result)
