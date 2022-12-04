from container_or_host import host_for_dependency
from pymongo import MongoClient
from pymongo.database import Database

__all__ = ["get"]

HOST = host_for_dependency(addres_for_docker="mongodb")
DSN = f"mongodb://usf:usf@{HOST}"
DATABASE = "negotiations"


_mongo_db: Database | None = None


def get() -> Database:
    global _mongo_db

    if _mongo_db is None:
        _mongo_db = getattr(MongoClient(DSN), DATABASE)

    return _mongo_db
