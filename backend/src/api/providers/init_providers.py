from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.middleware.auth import AuthenticationMiddleware
from src.api.providers import abstract
from src.api.web_config import WebConfig
from src.core.config import Config
from src.api.providers import common as common_provider
from src.api.providers import services


def bind_common(app: FastAPI, config: Config):
    app.dependency_overrides[abstract.common.session_provider] = common_provider.db_session(config)  # type: ignore
    app.dependency_overrides[abstract.common.redis_pool_provider] = common_provider.redis_pool_getter(config)  # type: ignore
    app.dependency_overrides[abstract.common.hasher_provider] = common_provider.hasher_getter  # type: ignore
    app.dependency_overrides[abstract.common.tm_provider] = common_provider.tm_getter  # type: ignore
    app.dependency_overrides[abstract.common.fm_provider] = common_provider.fm_getter(config)  # type: ignore
    app.dependency_overrides[abstract.common.redis_db_provider] = common_provider.redis_db_getter  # type: ignore


def bind_services(app: FastAPI):
    app.dependency_overrides[abstract.services.files_work_service_provider] = services.files_work_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.account_service_provider] = services.account_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.auth_service_provider] = services.auth_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.chat_service_provider] = services.chat_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.message_service_provider] = services.message_service_getter  # type: ignore
    app.dependency_overrides[abstract.services.contact_service_provider] = services.contact_service_getter  # type: ignore


def bind_middlewares(app: FastAPI, config: WebConfig):
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AuthenticationMiddleware)  # type: ignore


def bind_providers(app: FastAPI, config: Config):
    bind_common(app, config)
    bind_middlewares(app, config.web)
    bind_services(app)
