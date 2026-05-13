
from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from settings.base import BaseConfig, BASE_DIR
from settings.log import LogConfig


class KeyCloakConfig(BaseConfig):
    base_url:str= Field(alias='KC_BASE_URL')
    realm: str = Field(alias='KC_REALM')
    client_id: str = Field(alias='KC_APP_CLIENT_ID')
    client_secret: SecretStr = Field(alias='KC_APP_CLIENT_SECRET')


class Config(BaseConfig):

    model_config = SettingsConfigDict(
        yaml_file=BASE_DIR / 'config' / 'config.yaml'
    )

    keycloak: KeyCloakConfig = Field(default_factory=KeyCloakConfig)

    log: LogConfig = Field(default_factory=LogConfig)

