from sqlmodel import SQLModel
from src.models.models import Usuario
from src.database.connection import engine


def create_all_tables() -> None:
    SQLModel.metadata.create_all(bind=engine)


def create_one_table(model):
    # SQLModel.metadata.create_all(bind=engine, tables=[Usuario.__table__])
    SQLModel.metadata.create_all(bind=engine, tables=[model.__table__])


def drop_all_tables() -> None:
    SQLModel.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    # create_all_tables()
    create_one_table(Usuario)
