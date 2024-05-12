from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import insert, select, join
from sqlalchemy.ext.asyncio import AsyncSession


from src.db.pg import async_session_maker



class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError




class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            session: AsyncSession = session
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_one(self, id: int):
        async with async_session_maker() as session:
            session: AsyncSession = session
            response = select(self.model).where(self.model.id == id)
            res = await session.execute(response)
            return res.scalar_one().to_read_model()

    async def find_all(self):
        async with async_session_maker() as session:
            session: AsyncSession = session
            response = select(self.model)
            res = await session.execute(response)
            res = [row[0].to_read_model() for row in res.all()]
            return res
    
    async def get_by_filter(self, **filter):
        async with async_session_maker() as session:
            session: AsyncSession = session
            response = select(self.model).filter_by(**filter)
            res = await session.execute(response)
            res = [row[0].to_read_model() for row in res.all()]
            return res
    
    async def get_one_by_filter(self, **filter):
        async with async_session_maker() as session:
            session: AsyncSession = session
            response = select(self.model).filter_by(**filter)
            res = await session.execute(response)
            return res.scalar_one().to_read_model()


