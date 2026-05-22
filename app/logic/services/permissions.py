from abc import abstractmethod, ABC
from typing import Iterable

from settings.config import Config


class BasePermissionService(ABC):
    @abstractmethod
    async def list_permissions(self, role: str) -> Iterable[str]: ...



class ConfigPermissionService(BasePermissionService):
    config: Config

    async def list_permissions(self, role: str) -> Iterable[str]:
        # todo
        return ['demo_read_permission']