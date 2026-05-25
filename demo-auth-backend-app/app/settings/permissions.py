from pydantic import Field

from settings.base import BaseConfig


class RoleConfig(BaseConfig):
    title: str
    permissions: list[str]

class UserConfig(BaseConfig):
    username: str
    roles: list[str]

class RoleAliaasConfig(BaseConfig):

    user: str = 'user'
    manager: str = 'manager'
    admin: str = 'admin'
    auditor: str = 'auditor'

class PermissionConfig(BaseConfig):
    users:list[UserConfig]
    roles:list[RoleConfig]
    role_alias: RoleAliaasConfig = Field(default_factory=RoleAliaasConfig)