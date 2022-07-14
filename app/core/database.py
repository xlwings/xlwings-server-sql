from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .. import settings

engine = create_engine(
    settings.db_connection_string,
    pool_pre_ping=True,
    future=True,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.db_connection_string
    else {},
)


def get_db() -> Session:
    SessionLocal = sessionmaker(bind=engine, future=True)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
