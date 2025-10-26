from uuid import UUID

from availability.facade import Availability
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()


class ResourcePayload(BaseModel):
    resource_id: int
    owner_id: UUID

    class Config:
        schema_extra = {
            "example": {
                "resource_id": 0,
                "owner_id": "00000000-0000-0000-0000-000000000000",
            }
        }


@app.post("/resources")
def create_resource(payload: ResourcePayload) -> Response:
    Availability().register(owner_id=payload.owner_id, resource_id=payload.resource_id)
    return Response(status_code=201)


@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int) -> Response:
    Availability().unregister(resource_id=resource_id)
    return Response(status_code=204)


class LockingPayload(BaseModel):
    locking_party: UUID

    class Config:
        schema_extra = {
            "example": {
                "locking_party": "00000000-0000-0000-0000-000000000000",
            }
        }


@app.post("/resources/{resource_id}/lock")
def lock_resource(resource_id: int, payload: LockingPayload) -> Response:
    try:
        Availability().lock(resource_id=resource_id, lock_for=payload.locking_party)
    except Availability.AlreadyLocked:
        return Response(status_code=403)

    return Response(status_code=204)


@app.delete("/resources/{resource_id}/lock")
def unlock_resource(resource_id: int, payload: LockingPayload) -> Response:
    try:
        Availability().unlock(resource_id=resource_id, locked_by=payload.locking_party)
    except Availability.LockedBySomeoneElse:
        return Response(status_code=403)

    return Response(status_code=204)
