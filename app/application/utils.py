from fastapi import Depends, HTTPException
from starlette.requests import Request

from logic.services.keycloak import KeycloakClient


# Получаем токен из cookie
async def get_token_from_cookie(request: Request) -> str | None:
    return request.cookies.get("access_token")


# Получаем пользователя по токену
async def get_current_user(
        token: str,
        keycloak_client: KeycloakClient,
) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: No access token")

    try:
        user_info = await keycloak_client.get_user_info(token)
        return user_info
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid token")