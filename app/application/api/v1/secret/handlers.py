import logging
import pprint

from typing import Annotated
from colorama import Style, Fore
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.api.v1.dependencies import ContainerDependency, RequireRole
from application.api.v1.secret.schemas import EditSecretRequestSchema
from application.services.keycloak import KeycloakService
from settings.config import Config
from application.services.keycloak import KeycloakService, User

router = APIRouter(prefix="/secret")
security = HTTPBearer()

logger = logging.getLogger(__name__)


@router.get(
    path="",
)
async def read_secret_handler(
    container: ContainerDependency,
    # user: Annotated[User, Depends(RequireRole(required_role='any'))],
    # user: Annotated[User, Depends(RequireRole(required_role='auth-demo-app-user'))],
    user: Annotated[User, Depends(RequireRole(required_role='auth-demo-app-admin'))],
):

    logger.debug(f"{user=}")

    return dict(
        roles = user.roles,
        permissions = []
    )


# @router.post(
#     path="",
# )
# async def edit_secret_handler(
#     schema: EditSecretRequestSchema,
#     container: ContainerDependency,
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ):
#
#     keycloak_service: KeycloakService = container.resolve(KeycloakService)
#
#     logger.debug(credentials)
#
#     user_info = keycloak_service.get_current_user(credentials=credentials)
#
#     logger.debug(f"{user_info=}")
#
#     return {"set_secret": schema.data}

