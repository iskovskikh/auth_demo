from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel

from domain.user.entity import User, Role
from settings.base import BASE_DIR
from settings.config import Config


class RoleConfigSchema(BaseModel):
    title: str
    permissions: list[str]


class UserConfigSchema(BaseModel):
    username: str
    roles: list[str]


class ConfigSchema(BaseModel):
    roles: list[RoleConfigSchema]
    users: list[UserConfigSchema]


@dataclass
class UserLoaderService:
    config:Config

    def load_users_fom_file(self) -> list[User]:

        roles_dict: dict[str, Role] = {}

        for role in self.config.permissions.roles:
            roles_dict.update(
                {role.title: Role(title=role.title, permissions=role.permissions)}
            )

        user_list: list[User] = []

        for user in self.config.permissions.users:
            roles: list[Role] = []
            for role_title in user.roles:
                role: Role | None = roles_dict.get(role_title)
                if role:
                    roles.append(role)
            user_list.append(
                User(username=user.username, roles=roles),
            )

        return user_list
