import logging
from dataclasses import dataclass
from fastapi.security import HTTPAuthorizationCredentials
from keycloak import KeycloakOpenID, KeycloakError
from pydantic import BaseModel

from application.exceptions import ApplicationException
import logging
import pprint

from colorama import Style, Fore

from settings.config import Config


logger = logging.getLogger(__name__)


@dataclass(eq=False)
class UnauthorizedException(ApplicationException):
    details: str

    @property
    def message(self):
        return f'{self.details}'


@dataclass(eq=False)
class ForbiddenException(ApplicationException):
    details: str

    @property
    def message(self):
        return f'{self.details}'


class User(BaseModel):
    username: str | None
    roles: list[str]


@dataclass
class KeycloakService:
    keycloak_openid: KeycloakOpenID

    def require_roles(
        self,
        user: User,
        allowed_roles = list[str],
    ):
         if not (set(user.roles) & set(allowed_roles)):
             logger.debug(f'Не достаточно прав {user=} {allowed_roles=}')
             raise ForbiddenException("Не достаточно прав")


    def get_current_user(self, credentials: HTTPAuthorizationCredentials)->User:
        token = credentials.credentials
        logger.debug(f"{Style.DIM}{token}{Style.RESET_ALL}")
        try:
            payload = self.keycloak_openid.decode_token(
                token = token,
                validate= True,
            )

            for line in pprint.pformat(payload).split('\n'):
                logger.debug(f"{Style.DIM}{line}{Style.RESET_ALL}")

            return User(
                username =payload.get("preferred_username"),
                roles =payload.get("realm_access", {}).get("roles", [])
            )

        # except (KeycloakError, ValueError) as e:
        except Exception as e:
            logger.error(e)
            raise UnauthorizedException(details=f'Ощибка авторизации: {e}')

