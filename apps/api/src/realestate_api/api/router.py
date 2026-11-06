from fastapi import APIRouter

from realestate_api.api.routes import health, properties

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(properties.router)
