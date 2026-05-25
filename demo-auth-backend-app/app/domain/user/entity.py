from dataclasses import dataclass


@dataclass
class Role:
    title: str
    permissions: list[str]


@dataclass
class User:
    username: str
    roles: list[Role]
