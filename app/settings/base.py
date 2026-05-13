from pathlib import Path
from typing import Any

from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, EnvSettingsSource, PydanticBaseSettingsSource, YamlConfigSettingsSource, \
    SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class AliasOnlyEnvSettingsSource(EnvSettingsSource):
    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        # если у поля не задан alias или validation_alias,
        #  то не будет проверяться наличие env переменной для этого поля
        is_has_alias: bool = (field.alias is not None) or (field.validation_alias is not None)
        if not is_has_alias:
            return None, field_name, False

        return super().get_field_value(field=field, field_name=field_name)


class PydanticBaseSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # явно помечаем как неиспользуемые
        _ = env_settings, dotenv_settings, file_secret_settings
        return (
            init_settings,
            AliasOnlyEnvSettingsSource(settings_cls),
            # dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            # file_secret_settings,
        )


class BaseConfig(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter=None,
        extra="ignore"
    )