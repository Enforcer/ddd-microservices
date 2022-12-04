import pymongo
from catalog import db


def migrate() -> None:
    print("Applying migrations...")
    collection = getattr(db.get(), "catalog_items")
    collection.create_index(
        [
            ("item_id", pymongo.ASCENDING),
        ],
        unique=True,
    )
    collection.create_index(
        [
            ("title", pymongo.TEXT),
            ("description", pymongo.TEXT),
        ]
    )


if __name__ == "__main__":
    migrate()