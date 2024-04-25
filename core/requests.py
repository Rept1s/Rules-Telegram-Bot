from core import models
from sqlalchemy import select, insert, update


async def insert_user(user, username, first_name, last_name):
    async with models.async_session() as session:
        query = (
            insert(models.User)
            .values(user_id=user,
                    username=username or None,
                    user_first_name=first_name or None,
                    user_full_name=last_name or None)
        )
        await session.execute(query)
        await session.commit()


async def update_user(user, username, first_name, last_name):
    async with models.async_session() as session:
        query = (
            update(models.User)
            .values(user_id=user,
                    username=username or None,
                    user_first_name=first_name or None,
                    user_full_name=last_name or None)
        )
        await session.execute(query)
        await session.commit()


async def select_check_id(user):
    async with models.async_session() as session:
        query = (
            select(models.User.user_id)
            .select_from(models.User)
            .filter_by(user_id=user)
        )
        result = await session.execute(query)
        return result.scalar()
