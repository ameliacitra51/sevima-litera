from fastapi import APIRouter
from app.api.v1 import auth
from app.api.v1 import courses, lessons
from app.api.v1 import health

api_router = APIRouter()

# Register endpoint modules
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router)
api_router.include_router(courses.router)
api_router.include_router(lessons.router)
