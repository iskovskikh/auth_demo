import logging
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import Iterable

from settings.config import Config


logger = logging.getLogger(__name__)


class BasePermissionService(ABC):
    @abstractmethod
    async def list_permissions(self, role: str) -> Iterable[str]: ...


@dataclass
class ConfigPermissionService(BasePermissionService):
    config: Config

    permissions_index: dict[str, list[str]] = field(init=False)

    def __post_init__(self):
        self.permissions_index = {
            role.title: role.permissions
            for role in (
                self.config.permissions.roles
            )
        }
        logger.debug(f"{self.permissions_index=}")

    async def list_permissions(self, role: str) -> Iterable[str]:
        return self.permissions_index.get(role, [])
