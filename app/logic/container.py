from anyio.functools import lru_cache
from httpx import AsyncClient
from punq import Container, Scope

from logic.services.keycloak import KeycloakClient


@lru_cache(1)
def get_container()-> Container:

    return _init_container()


def _init_container() -> Container:

    container = Container()

    container.register(AsyncClient)
    container.register(KeycloakClient, factory=KeycloakClient, scope=Scope.singleton)

    return container