import re
import sys
import urllib.parse
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_connection_string: str
    google_allowed_domains: List

    class Config:
        env_file = ".env"


settings = Settings()

# Driver tweaks
settings.db_connection_string = (
    settings.db_connection_string.replace("postgres://", "postgresql://")
    .replace("mysql://", "mysql+pymysql://")
    .replace("mariadb://", "mariadb+pymysql://")
)

if settings.db_connection_string.startswith("mssql"):
    settings.db_connection_string += "?driver=ODBC+Driver+17+for+SQL+Server"
elif settings.db_connection_string.startswith("oracle"):
    # This is only required for SQLAlchemy < 2.0, see:
    # https://levelup.gitconnected.com/using-python-oracledb-1-0-with-sqlalchemy-pandas-django-and-flask-5d84e910cb19
    import oracledb

    oracledb.version = "8.3.0"
    sys.modules["cx_Oracle"] = oracledb

# URL encoded password
pattern = re.compile(r"(.*)://[^:]*:(.*)@")
match = pattern.match(settings.db_connection_string)
if match:
    password = match.group(2)
    connection_string_parts = settings.db_connection_string.split(password)
    connection_string_parts.insert(1, urllib.parse.quote_plus(password))
    settings.db_connection_string = "".join(connection_string_parts)
