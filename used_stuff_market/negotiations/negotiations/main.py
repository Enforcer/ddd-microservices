from container_or_host import host_for_dependency
from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration
from negotiations.application.availability_port import AvailabilityPort
from negotiations.application.repository import NegotiationsRepository
from negotiations.infrastructure import db
from negotiations.infrastructure.availability_client import AvailabilityClient
from negotiations.infrastructure.mongo_repository import MongoDbNegotiationsRepository
from pymongo.database import Database

container = Container()
container[Database] = lambda: db.get()
container[NegotiationsRepository] = MongoDbNegotiationsRepository  # type: ignore


def availability_factory() -> AvailabilityClient:
    availability_host = host_for_dependency(addres_for_docker="availability")
    base_url = f"http://{availability_host}:8300"
    return AvailabilityClient(base_url=base_url)


container[AvailabilityPort] = availability_factory  # type: ignore


deps = FastApiIntegration(container)
