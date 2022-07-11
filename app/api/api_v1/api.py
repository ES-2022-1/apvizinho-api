from fastapi import APIRouter

from .endpoints import address, announcement, user, vacancy

api_router = APIRouter()

api_router.include_router(announcement.router, prefix="/announcement", tags=["Announcement"])
api_router.include_router(address.router, prefix="/address", tags=["Address"])
api_router.include_router(vacancy.router, prefix="/vacancy", tags=["Vacancy"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
