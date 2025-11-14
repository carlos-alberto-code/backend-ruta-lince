import os
from typing import Generator
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.sqlite")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)


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
