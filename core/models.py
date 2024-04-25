from environs import Env
from sqlalchemy import BigInteger, delete
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from core.settings import get_database

engine = create_async_engine('sqlite+aiosqlite:////' + get_database().database, echo=False)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(nullable=True)
    user_first_name: Mapped[str] = mapped_column(nullable=True)
    user_full_name: Mapped[str] = mapped_column(nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
