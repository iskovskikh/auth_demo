import logging
from pprint import pformat
from typing import TypeVar

from colorama import Fore, Style

from settings.base import BaseConfig

logger = logging.getLogger(__name__)

BaseConfigType = TypeVar('BaseConfigType', bound=BaseConfig)

def print_config(config: BaseConfigType):
    for line in pformat(config.model_dump(), indent=2).split('\n'):
        logger.debug(f'{Fore.LIGHTWHITE_EX}{line}{Style.RESET_ALL}')