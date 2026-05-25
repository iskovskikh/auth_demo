import logging

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from application.api.v1.dependencies import ContainerDependency, RequireRole
from application.api.v1.secret.schemas import EditSecretRequestSchema
from application.services.keycloak import User
from infra.repositories.secret import SecretRepository
from settings.config import Config, get_config


logger = logging.getLogger(__name__)

router = APIRouter()
config: Config = get_config()

@router.get(
    path="/public",
)
async def read_secret_handler(
    container: ContainerDependency,
    user: Annotated[User, Depends(RequireRole())],
):
    return {"public_data": "999"}


@router.get(
    path="/secret",
)
async def read_secret_handler(
    container: ContainerDependency,
    user: Annotated[
        User,
        Depends(
            RequireRole(
                allowed_roles=(
                    config.permissions.role_alias.user,
                    config.permissions.role_alias.admin,
                ),
            ),
        ),
    ],
):

    logger.debug(f"{user=}")

    repo: SecretRepository = container.resolve(SecretRepository)

    value: str = repo.get()

    return {"secret_read": value}


@router.post(
    path="/secret",
)
async def edit_secret_handler(
    schema: EditSecretRequestSchema,
    container: ContainerDependency,
    user: Annotated[
        User,
        Depends(
            RequireRole(
                allowed_roles=(
                    config.permissions.role_alias.admin,
                ),
            ),
        ),
    ],
):
    logger.debug(f"{user=}")
    logger.debug(f"{schema.value=}")

    repo: SecretRepository = container.resolve(SecretRepository)

    repo.set(new_value=schema.value)
    value: str = repo.get()

    return {"secret_edit": value}
