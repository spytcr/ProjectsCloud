import sqlite3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

database = SQLAlchemy()


@event.listens_for(Engine, 'connect')
def _register_unicode_lower(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        dbapi_connection.create_function('lower', 1, str.lower, deterministic=True)
