import logging

from colorama import Style
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.api.v1.dependencies import ContainerDependency
from application.api.v1.secret.schemas import EditSecretRequestSchema
from logic.services.keycloak import KeycloakService

router = APIRouter(prefix="/secret")
security = HTTPBearer()

logger = logging.getLogger(__name__)


@router.get(
    path="",
)
async def read_secret_handler(
    container: ContainerDependency,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    keycloak_service: KeycloakService = container.resolve(KeycloakService)

    logger.debug(credentials)

    user_info = keycloak_service.get_current_user(credentials=credentials)
    logger.debug(f"{Style.DIM}{user_info=}{Style.RESET_ALL}")

    roles: list[str] = user_info["realm_access"]["roles"]
    permissions:list[str] = []

    logger.debug(f"{roles=}")
    logger.debug(f"{permissions=}")

    return dict(
        roles = roles,
        permissions = permissions
    )


@router.post(
    path="",
)
async def edit_secret_handler(
    schema: EditSecretRequestSchema,
    container: ContainerDependency,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    keycloak_service: KeycloakService = container.resolve(KeycloakService)

    logger.debug(credentials)

    user_info = keycloak_service.get_current_user(credentials=credentials)

    logger.debug(f"{user_info=}")

    return {"set_secret": schema.data}
