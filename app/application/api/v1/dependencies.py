from typing import Annotated

from fastapi import Depends
from punq import Container

from logic.container import get_container

ContainerDependency = Annotated[Container, Depends(get_container)]
