from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from dishka.integrations.fastapi import setup_dishka

from src.api import router as api_router
from src.core.config import settings
from src.core.models.db_helper import db_helper
from src.core.dependencies.container import container


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

setup_dishka(container=container, app=app)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
