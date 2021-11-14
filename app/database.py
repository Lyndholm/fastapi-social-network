from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import config

SQLACLCHEMY_DATABASE_URL = (
    f"postgresql://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}"
    f"@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}"
)

engine = create_engine(SQLACLCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
