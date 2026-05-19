from dataclasses import dataclass
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from keycloak import KeycloakOpenID, KeycloakError
from starlette import status


@dataclass
class KeycloakService:
    keycloak_openid: KeycloakOpenID

    def get_current_user(self, credentials: HTTPAuthorizationCredentials):
        token = credentials.credentials

        try:
            # Валидация токена
            user_info = self.keycloak_openid.decode_token(
                token,
                self.keycloak_openid.public_key(),
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "verify_exp": True,
                },
            )

            return user_info

        except KeycloakError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
