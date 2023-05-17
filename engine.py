import urllib

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config import Config


def sqlite_engine() -> Engine:
    p = Path(__file__).parent / 'speedtest.db'
    p.touch(exist_ok=True)
    return create_engine(f'sqlite:///{str(p.absolute())}', echo=True)


def mysql_engine() -> Engine:
    config = Config()

    db_hostname = config.get('DB_HOSTNAME')
    db_username = config.get('DB_USERNAME')
    db_password = config.get('DB_PASSWORD')
    db_database = config.get('DB_DATABASE')
    return create_engine(
        f'mysql+mysqldb://{db_username}:{urllib.parse.quote_plus(db_password)}@{db_hostname}/{db_database}',
        echo=True,
    )


# engine = sqlite_engine()
engine = mysql_engine()
