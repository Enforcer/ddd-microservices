import pymongo
from orchestrator import db


def migrate() -> None:
    print("Applying migrations...")
    collection = getattr(db.get(), "process_manager_adding_new_item")
    collection.create_index(
        [
            ("item_id", pymongo.ASCENDING),
        ],
        unique=True,
    )


if __name__ == "__main__":
    migrate()
