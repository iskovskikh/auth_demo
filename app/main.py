from settings.config import Config
from settings.logger import init_logger, get_logger_config
from colorama import init as init_colorama

from settings.urils import print_config


def main():
    print("Hello from auth-demo!")


if __name__ == "__main__":
    config = Config()
    init_colorama()
    init_logger(config=config)
    print_config(config=config)
    main()
