from pathlib import Path

from pydantic import Field

from settings.base import BaseConfig, BASE_DIR


class LogConfig(BaseConfig):
	logger_config_path: Path = BASE_DIR / 'config' / 'logger_config.yaml'
	path: Path = BASE_DIR / 'logs'
	console_format: str = Field(
		# default='%(levelname) -10s %(asctime)s %(name) -30s %(module) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
        default='%(levelname)s | %(message)s'
	)
	file_format: str = Field(
		default='%(levelname) -10s %(asctime)s %(name) -30s %(module) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
	)
