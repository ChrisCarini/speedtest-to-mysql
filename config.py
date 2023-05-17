import os

from pathlib import Path

import yaml

from log import logger

CHECKED_ENVIRONMENT_VARIABLES = [
    'SERVER_ID',
    'DB_HOSTNAME',
    'DB_USERNAME',
    'DB_PASSWORD',
    'DB_DATABASE',
]

OOKLA_SPEEDTEST_CLI_EULA_FILE = '~/.config/ookla/speedtest-cli.json'

CONFIG_FILE = 'config.yaml'

GSHEET_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class Config:
    def __init__(self) -> None:
        if not Path(CONFIG_FILE).exists():
            logger.critical(f'Config file {CONFIG_FILE} does not exist. Exiting.')
            exit(1)
        logger.info(f'Loading configuration from [{CONFIG_FILE}]...')
        with open(CONFIG_FILE, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.SafeLoader)

    def get(self, key: str, default: str = '') -> str:
        """Get the configuration value for the provided key. If none found, return the default.

        :param key: The configuration key
        :param default: The default value, should no value be set in the configuration
        :return: The configuration value, or 'default' value should one not be set.
        """

        return str(self.config.get(key, os.environ.get(key, default)))


if __name__ == '__main__':
    config = Config()
    print(config)
