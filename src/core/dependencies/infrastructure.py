from typing import AsyncGenerator

from dishka import (
    Provider, 
    Scope, 
    provide
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.db_helper import db_helper


class InfrastructureProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with db_helper.session_factory() as session:
            yield session


