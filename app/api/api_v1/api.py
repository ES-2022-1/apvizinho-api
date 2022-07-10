from fastapi import APIRouter

from .endpoints import local, address, room

api_router = APIRouter()

api_router.include_router(local.router, prefix="/local", tags=["local"])
api_router.include_router(address.router, prefix="/address", tags=["address"])
api_router.include_router(room.router, prefix="/room", tags=["room"])
