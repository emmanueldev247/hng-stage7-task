from fastapi import FastAPI

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.keys import router as keys_router
from app.api.routes.users import router as users_router
from app.api.routes.service import router as service_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="Mini Authentication + API Key System",
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(keys_router)
    app.include_router(users_router)
    app.include_router(service_router)

    return app


app = create_app()
