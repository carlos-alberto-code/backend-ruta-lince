import os
from typing import Generator
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

DATABASE_URL_PRE = os.getenv("DATABASE_URL_PRE", "sqlite:///:memory:")

engine = create_engine(DATABASE_URL_PRE)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
