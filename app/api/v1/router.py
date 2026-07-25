from fastapi import APIRouter

from app.api.v1.endpoints import health

router: APIRouter = APIRouter(prefix="/v1")

router.include_router(health.router)
