from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from domain.user.entity import User
from infra.services.user import UserLoaderService


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...


@dataclass
class InmemoryUserRepository(BaseUserRepository):
    user_loader_service: UserLoaderService
    _user_list: list[User]

    def __post_init__(self):
        self._user_list = self.user_loader_service.load_users_fom_file()

    async def get_by_username(self, username: str) -> User | None:
        try:
            return next(user for user in self._user_list if user.username == username)
        except StopIteration:
            return None
