from settings.base import BaseConfig

class RoleConfig(BaseConfig):
    label: str
    permissions: list[str]


class PermissionConfig(BaseConfig):
    user: RoleConfig
    manager: RoleConfig
    admin: RoleConfig
    auditor: RoleConfig
