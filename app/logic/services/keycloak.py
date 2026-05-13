from dataclasses import dataclass
from fastapi import HTTPException

from httpx import AsyncClient, RequestError
from pydantic import BaseModel, AnyUrl

from settings.config import Config


@dataclass
class TokensDto: ...


class KeycloakRequestSchema(BaseModel):
    grand_type: str = "authorization_code"
    code: str
    redirect_uri: AnyUrl
    client_id: str
    client_secret: str


@dataclass
class KeycloakClient:
    client: AsyncClient
    config: Config

    async def get_tokens(self, code: str) -> TokensDto:

        payload: KeycloakRequestSchema = KeycloakRequestSchema(
            code=code,
            redirect_uri=self.config.auth.redirect_uri,
            client_id=self.config.keycloak.client_id,
            client_secret=self.config.keycloak.client_secret.get_secret_value(),
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = await self.client.post(
                url=self.config.keycloak.token_url,
                data=payload.model_dump(),
                headers=headers,
            )
            if response.status_code != 200:
                raise HTTPException(  # todo: переделать exception
                    status_code=401, detail=f"Token request failed: {response.text}"
                )
            return response.json()
        except RequestError as e:
            raise HTTPException(  # todo: переделать exception
                status_code=500, detail=f"Token exchange failed: {str(e)}"
            )

        return TokensDto()

    async def get_user_info(self, token: str) -> dict:
        
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await self.client.get(self.config.keycloak.userinfo_url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401, detail=f"Invalid access token: {response.text}"
                )
            return response.json()
        except RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Keycloak request error: {str(e)}"
            )