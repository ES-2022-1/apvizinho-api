from fastapi import APIRouter

from .endpoints import address, local, room, user

api_router = APIRouter()

api_router.include_router(local.router, prefix="/local", tags=["local"])
api_router.include_router(address.router, prefix="/address", tags=["address"])
api_router.include_router(room.router, prefix="/room", tags=["room"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
