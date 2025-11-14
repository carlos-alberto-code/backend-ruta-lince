from typing import Generator
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("sqlite:///../src/database/database.sqlite")
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
