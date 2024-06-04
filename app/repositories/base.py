from typing import Any
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, func, or_, desc


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, values):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, limit: int, offset: int):
        raise NotImplementedError

    @abstractmethod
    async def update(self, _id: int, values):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, _id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, ABC):
    model: Any

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, values: dict):
        stmt = insert(self.model).values(**values).returning(self.model)
        result = await self.session.execute(stmt)
        result = result.scalar_one()
        return result

    async def get(self, **filters) -> Any:
        stmt = select(self.model).filter_by(**filters).limit(1)
        result = await self.session.execute(stmt)
        result = result.scalars().all()
        if len(result) == 0:
            return None
        result = result[0]
        return result

    async def get_list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
        reverse: bool = False,
        **filters,
    ) -> dict:
        total_count_stmt = select(func.count()).select_from(self.model)
        stmt = select(self.model)

        for key, value in filters.items():
            if isinstance(value, list):
                stmt_filter = or_(*[getattr(self.model, key) == v for v in value])
                total_count_stmt = total_count_stmt.where(stmt_filter)
                stmt = stmt.where(stmt_filter)
            elif value is not None:
                total_count_stmt = total_count_stmt.filter_by(**{key: value})
                stmt = stmt.filter_by(**{key: value})

        total_count = await self.session.scalar(total_count_stmt)

        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        if order_by is not None:
            stmt = stmt.order_by(desc(order_by)) if reverse else stmt.order_by(order_by)
        result = await self.session.execute(stmt)
        result = result.scalars().all()

        response = {
            'total': total_count,
            'limit': limit,
            'offset': offset,
            'data': result
        }
        return response

    async def update(self, _id: int, values: dict):
        await self.session.execute(update(self.model).where(self.model.id == _id).values(**values))
        return await self.get(id=_id)

    async def delete(self, _id: int):
        stmt = delete(self.model).where(self.model.id == _id)
        await self.session.execute(stmt)
