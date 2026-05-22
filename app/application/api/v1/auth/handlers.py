import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from application.api.v1.dependencies import ContainerDependency, RequireRole
from application.api.v1.auth.schemas import ProfileResponseSchema
from application.services.keycloak import User
from logic.services import permissions
from logic.services.permissions import BasePermissionService
from settings.config import Config

security = HTTPBearer()

router = APIRouter(prefix="/auth")

logger = logging.getLogger(__name__)

@router.get(
    path="/profile",
)
async def get_profile_handler(
    container: ContainerDependency,
    user: Annotated[User, Depends(RequireRole())],
) -> ProfileResponseSchema:

    config = container.resolve(Config)

    permission_service: BasePermissionService = container.resolve(BasePermissionService)

    permission_list = []

    for role in user.roles:
        permissions_for_role = await permission_service.list_permissions(role)
        permission_list.extend(permissions_for_role)

    return ProfileResponseSchema(
        username = user.username,
        roles = user.roles,
        permissions = list(set(permission_list)),
    )