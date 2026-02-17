from fastapi import FastAPI

from src.api.handlers.bind_routers import bind_exceptions_handlers, bind_routes
from src.api.providers.init_providers import bind_providers
from src.core.config import Config


def init_app(app: FastAPI, config: Config) -> FastAPI:
    bind_providers(app, config)
    bind_exceptions_handlers(app)
    bind_routes(app, config.web)

    return app
