from anyio.functools import lru_cache
from punq import Container, Scope
from keycloak import KeycloakOpenID
from logic.services.keycloak import KeycloakService
from settings.config import Config


@lru_cache(maxsize=1)
def get_container() -> Container:

    return _init_container()


def get_keycloak_client(config: Config) -> KeycloakOpenID:

    return KeycloakOpenID(
        server_url=config.keycloak.base_url,  # "http://localhost:8080/",
        client_id=config.keycloak.client_id,  # "my-client",
        realm_name=config.keycloak.realm,
        client_secret_key=config.keycloak.client_secret.get_secret_value(),
    )


def _init_container() -> Container:

    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config = container.resolve(Config)

    container.register(KeycloakOpenID, instance=get_keycloak_client(config=config), scope=Scope.singleton)
    container.register(KeycloakService, factory=KeycloakService, scope=Scope.singleton)

    return container
