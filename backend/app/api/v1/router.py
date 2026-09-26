from fastapi import APIRouter

from app.api.v1 import admin_catalog, auth, courses, health, lessons

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router)
api_router.include_router(admin_catalog.router)
api_router.include_router(courses.router)
api_router.include_router(lessons.router)
