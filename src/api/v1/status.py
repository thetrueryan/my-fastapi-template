from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/status")
async def get_status(
    session: FromDishka[AsyncSession]
):
    return {"status": "ok"}
