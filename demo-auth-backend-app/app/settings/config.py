from functools import lru_cache

from pydantic import Field, SecretStr, AnyUrl
from pydantic_settings import SettingsConfigDict

from settings.base import BaseConfig, BASE_DIR
from settings.log import LogConfig
from settings.permissions import PermissionConfig


class KeyCloakConfig(BaseConfig):
    base_url: str = Field(alias="KC_BASE_URL")
    realm: str = Field(alias="KC_REALM")
    client_id: str = Field(alias="KC_APP_CLIENT_ID")
    client_secret: SecretStr = Field(alias="KC_APP_CLIENT_SECRET")

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/token"

    @property
    def auth_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/auth"

    @property
    def logout_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/logout"

    @property
    def userinfo_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/userinfo"


class AuthConfig(BaseConfig):
    base_url: str = "localhost:8000"

    @property
    def redirect_uri(self) -> AnyUrl:
        return AnyUrl(f"{self.base_url}/api/login/callback")


class Config(BaseConfig):
    model_config = SettingsConfigDict(yaml_file=BASE_DIR / "config" / "config.yaml")

    keycloak: KeyCloakConfig = Field(default_factory=KeyCloakConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    permissions: PermissionConfig = Field(default_factory=PermissionConfig)

    log: LogConfig = Field(default_factory=LogConfig)

@lru_cache(maxsize=1)
def get_config()-> Config:
    return Config()