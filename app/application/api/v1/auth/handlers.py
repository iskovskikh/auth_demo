


import logging
import pprint
from typing import Annotated
from colorama import Style, Fore
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from application.api.v1.dependencies import ContainerDependency, RequireRole
from application.api.v1.auth.schemas import ProfileResponseSchema
from application.api.v1.dependencies import ContainerDependency, require_role
from application.api.v1.secret.schemas import EditSecretRequestSchema
from application.services.keycloak import KeycloakService, User
from settings.config import Config
from application.services.keycloak import KeycloakService, User

security = HTTPBearer()

router = APIRouter(prefix="/auth")

logger = logging.getLogger(__name__)

@router.get(
    path="/profile",
)
async def get_profile_handler(
    container: ContainerDependency,
    user: Annotated[User, Depends(RequireRole(required_role='any'))],
) -> ProfileResponseSchema:

    config = container.resolve(Config)

    return ProfileResponseSchema(
        username = user.username,
        roles = user.roles,
        permissions = [],
    )