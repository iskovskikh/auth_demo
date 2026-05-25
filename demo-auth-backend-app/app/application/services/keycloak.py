import logging
from dataclasses import dataclass
from fastapi.security import HTTPAuthorizationCredentials
from keycloak import KeycloakOpenID
from pydantic import BaseModel
from infra.repositories.user import BaseUserRepository
from application.exceptions import ApplicationException
import pprint

from colorama import Style


logger = logging.getLogger(__name__)


@dataclass(eq=False)
class UnauthorizedException(ApplicationException):
    details: str

    @property
    def message(self):
        return f"{self.details}"


@dataclass(eq=False)
class ForbiddenException(ApplicationException):
    details: str

    @property
    def message(self):
        return f"{self.details}"


class User(BaseModel):
    username: str | None
    roles: list[str]


@dataclass
class KeycloakService:
    keycloak_openid: KeycloakOpenID
    user_repository: BaseUserRepository

    def require_roles(
        self,
        user: User,
        allowed_roles=list[str],
    ):
        logger.debug(f"{set(user.roles)=}")
        logger.debug(f"{set(allowed_roles)=}")
        logger.debug(f"{set(user.roles) & set(allowed_roles)=}")
        if "any" not in allowed_roles and not (set(user.roles) & set(allowed_roles)):
            logger.debug(f"Не достаточно прав {user=} {allowed_roles=}")
            raise ForbiddenException("Не достаточно прав")

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials) -> User:
        token = credentials.credentials
        logger.debug(f"{Style.DIM}{token}{Style.RESET_ALL}")
        try:
            payload = self.keycloak_openid.decode_token(
                token=token,
                validate=True,
            )

            for line in pprint.pformat(payload).split("\n"):
                logger.debug(f"{Style.DIM}{line}{Style.RESET_ALL}")

            # роли из токена keycloak
            # return User(
            #     username =payload.get("preferred_username"),
            #     roles =payload.get("realm_access", {}).get("roles", [])
            # )

            # роли из репозитория
            username: str = payload.get("preferred_username")
            if not username:
                raise UnauthorizedException(details="username пустой")
            user: User | None = await self.user_repository.get_by_username(
                username=username
            )

            if not user:
                raise UnauthorizedException(details="Не удалось найти пользователя")

            return User(
                username=username,
                roles=[role.title for role in user.roles],
            )

        # except (KeycloakError, ValueError) as e:
        except Exception as e:
            logger.error(e)
            raise UnauthorizedException(details=f"Ощибка авторизации: {e}")
