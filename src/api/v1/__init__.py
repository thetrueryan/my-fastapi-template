from fastapi import APIRouter

from src.api.v1 import status, hysteria
from src.core.config import settings

router = APIRouter()

router.include_router(
    status.router,
    prefix=settings.api.v1.prefix,
    tags=["status"],
)

router.include_router(
    hysteria.router,
    prefix=settings.api.v1.prefix,
)
