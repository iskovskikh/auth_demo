import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from application.api.v1.secret.handlers import router as secret_router

from settings.config import Config
from settings.logger import init_logger
from colorama import init as init_colorama

from settings.urils import print_config

origins = [
    "http://localhost:3000",
]

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(secret_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        # allow_credentials=False,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return app


if __name__ == "__main__":
    config = Config()
    init_colorama()
    init_logger(config=config)
    print_config(config=config)

    uvicorn.run(
        "main:create_app",
        host="0.0.0.0",
        port=8000,
        # log_level="info",
        factory=True,
    )
