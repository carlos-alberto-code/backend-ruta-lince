from typing import Generic, TypeVar

from sqlmodel import SQLModel
from sqlmodel import and_, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.connection import get_session

T = TypeVar('T', bound=SQLModel)


def create(entity: T) -> None:
    try:
        with get_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
    except IntegrityError as e:
        session.rollback()
        raise SQLAlchemyError(f"Error de integridad: {e.orig}") from e


def delete(entity: T) -> None:
    try:
        with get_session() as session:
            session.delete(entity)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise SQLAlchemyError(f"Error al eliminar la entidad: {e}") from e


def update(entity: T) -> None:
    try:
        with get_session() as session:
            session.merge(entity)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise SQLAlchemyError(f"Error al actualizar la entidad: {e}") from e


class Repository(Generic[T]):

    def __init__(self, model: type[T]) -> None:
        super().__init__()
        self._model = model

    def get_by(self, *conditions) -> list[T] | None:
        try:
            with get_session() as session:
                stmt = select(self._model).where(and_(*conditions))
                result = session.exec(stmt)
                return list(result.all())
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error al obtener la entidad: {e}") from e

    def get_by_id(self, model_id: int) -> T | None:
        try:
            with get_session() as session:
                return session.get(self._model, model_id)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error al obtener la entidad mediante el ID: {e}") from e

    def get_all(self, page_size: int = 50, offset: int = 0) -> list[T]:
        try:
            with get_session() as session:
                stmt = select(self._model).offset(offset).limit(page_size)
                result = session.exec(stmt)
                return list(result.all())
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Error al obtener todas las entidades: {e}") from e
