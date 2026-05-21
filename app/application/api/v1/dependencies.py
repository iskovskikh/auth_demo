import logging
from dataclasses import dataclass
from functools import wraps
from typing import Annotated, Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from punq import Container

from application.services.keycloak import KeycloakService, User
from logic.container import get_container

logger = logging.getLogger(__name__)
ContainerDependency = Annotated[Container, Depends(get_container)]

security = HTTPBearer()


def require_role(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.debug(f'{role=}')

            # todo: ...

            return await func(*args, **kwargs)
        return wrapper
    return decorator

@dataclass(frozen=True)
class RequireRole:
    required_role: str

    def __call__(
        self,
        container: ContainerDependency,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:

        keycloak_service: KeycloakService = container.resolve(KeycloakService)
        user: User = keycloak_service.get_current_user(credentials=credentials)
        keycloak_service.require_roles(
            user=user,
            allowed_roles=[self.required_role],
        )

        return user
