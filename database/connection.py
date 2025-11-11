import os
from dotenv import load_dotenv
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL_PRE = os.getenv("DATABASE_URL_PRE", "sqlite+aiosqlite:///:memory:")

engine = create_async_engine(DATABASE_URL_PRE)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
