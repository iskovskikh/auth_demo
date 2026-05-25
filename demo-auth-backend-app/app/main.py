import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from application.api.exception_handlers import (
    unauthorized_exception_handler,
    application_exception_handler,
    request_validation_error_handler,
    forbidden_exception_handler,
)
from application.api.v1.secret.handlers import router as secret_router
from application.api.v1.auth.handlers import router as auth_router
from application.exceptions import ApplicationException
from application.services.keycloak import UnauthorizedException, ForbiddenException

from settings.config import Config
from settings.logger import init_logger
from colorama import init as init_colorama

from settings.urils import print_config

origins = [
    "http://localhost:3000",
]


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        # allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(secret_router)

    # exception handlers
    app.exception_handler(UnauthorizedException)(unauthorized_exception_handler)
    app.exception_handler(ForbiddenException)(forbidden_exception_handler)
    app.exception_handler(ApplicationException)(application_exception_handler)
    app.exception_handler(RequestValidationError)(request_validation_error_handler)

    return app


if __name__ == "__main__":
    config = Config()

    init_logger(config=config)
    init_colorama()
    print_config(config=config)

    uvicorn.run(
        "main:create_app",
        host="0.0.0.0",
        port=8000,
        # log_level="info",
        factory=True,
    )
