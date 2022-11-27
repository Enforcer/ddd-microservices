import pymongo
from negotiations import db
from pymongo.errors import DuplicateKeyError


def migrate() -> None:
    print("Applying migrations...")
    collection = getattr(db.get(), "negotiations")
    collection.create_index(
        [
            ("buyer_id", pymongo.ASCENDING),
            ("item_id", pymongo.ASCENDING),
            ("seller_id", pymongo.ASCENDING),
        ],
        unique=True,
    )


if __name__ == "__main__":
    migrate()
