from __future__ import annotations

from typing import Any, Callable, Coroutine, List, Self, Union, overload

from curio.meta import awaitable
from sqlalchemy.orm import DeclarativeMeta as DeclarativeMeta_
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import ColumnExpressionArgument

from .decorators import awaitableClassMethod


class ModelBase(object):
    query: Query
    session: Session

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.query = cls.db.session.query(cls)
        obj.session = cls.db.session
        return obj

    def new(cls: Self, **kwargs) -> Self:
        obj: cls = cls(**kwargs)
        obj.save()
        return obj

    @classmethod
    @awaitableClassMethod(new)
    def new(cls, **kwargs) -> Union[Coroutine[Any, Any, Self], Self]:
        async def inner():
            obj: cls = cls(**kwargs)
            await obj.save()
            return obj

        return inner()

    def get_all(cls, *criterion: ColumnExpressionArgument[bool], **kwargs: Any) -> List[Self]:
        if criterion:
            return cls.query.filter(*criterion, **kwargs).all()
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    @awaitableClassMethod(get_all)
    def get_all(
        cls, *criterion: ColumnExpressionArgument[bool], **kwargs: Any
    ) -> Union[Coroutine[Any, Any, List[Self]], List[Self]]:
        async def inner():
            if criterion:
                return cls.query.filter(*criterion, **kwargs).all()
            return cls.query.filter_by(**kwargs).all()

        return inner()

    @classmethod
    def get(cls, *criterion: ColumnExpressionArgument[bool], **kwargs: Any) -> Self:
        if criterion:
            return cls.query.filter(*criterion, **kwargs).first()
        return cls.query.filter_by(**kwargs).first()

    @awaitableClassMethod(get)
    @classmethod
    def get(
        cls, *criterion: ColumnExpressionArgument[bool], **kwargs: Any
    ) -> Union[Coroutine[Any, Any, Self], Self]:
        async def inner():
            if criterion:
                return await cls.query.filter(*criterion, **kwargs).first()
            return await cls.query.filter_by(**kwargs).first()

        return inner()

    def save(self) -> None:
        self.session.add(self)
        self.session.commit()

    @awaitable(save)
    async def save(self) -> None:
        with self.session.begin():
            self.session.add(self)
            await self.session.commit()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    @awaitable(update)
    async def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        await self.save()

    def delete(self):
        self.session.delete(self)
        self.session.commit()

    @awaitable(delete)
    async def delete(self):
        with self.session.begin():
            self.session.delete(self)
            await self.session.commit()
