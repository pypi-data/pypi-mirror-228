from __future__ import annotations

import logging
import secrets
import warnings
from contextlib import ExitStack
from contextvars import ContextVar, Token
from pprint import pformat, pprint
from typing import Any, Callable, Dict, List, Literal, Optional, Self, Tuple, Type, Union, overload

from fastapi import FastAPI
from sqlalchemy import MetaData, create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import DeclarativeMeta as DeclarativeMeta_
from sqlalchemy.orm import Query, Session, declarative_base, sessionmaker
from sqlalchemy.sql import ColumnExpressionArgument
from sqlalchemy.types import BigInteger, Integer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from .exceptions import SessionNotInitialisedError, SQLAlchemyAsyncioMissing
from .types import ModelBase

try:
    from sqlalchemy.ext import asyncio

    sqlalchemy_asyncio = True
except ImportError:
    sqlalchemy_asyncio = False
try:
    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
        AsyncSession,
        async_sessionmaker,
        create_async_engine,
    )
except ImportError:
    create_async_engine = None
    async_sessionmaker = None

_session = ContextVar("_session", default=None)


class DBSession:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def __enter__(self):
        if not isinstance(self.db.session_maker, sessionmaker):
            raise SessionNotInitialisedError
        self.token = _session.set(self.db.session_maker(**self.db.session_args))
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        sess = self.db.session
        try:
            if exc_type is not None:
                sess.rollback()

            elif self.db.commit_on_exit:
                sess.commit()
        except:
            sess.close()
            _session.reset(self.token)

    async def __aenter__(self):
        if not isinstance(self.db.session_maker, async_sessionmaker):
            raise SessionNotInitialisedError
        self.token = _session.set(self.db.session_maker(**self.db.session_args))
        return self.db

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.db.session
        try:
            if exc_type is not None:
                self.db.session.rollback()
            elif self.db.commit_on_exit:
                self.db.session.commit()
        except:
            await self.db.session.close()
            _session.reset(self.token)


class SQLAlchemy:
    def __init__(
        self,
        url: Optional[URL] = None,
        *,
        custom_engine: Optional[Engine] = None,
        engine_args: Dict[str, Any] = None,
        session_args: Dict[str, Any] = None,
        commit_on_exit: bool = False,
        verbose: Literal[0, 1, 2, 3] = 0,
        async_: bool = False,
        expire_on_commit: Optional[bool] = False,
        extended: bool = True,
        _session_manager: DBSession = DBSession,
    ):
        self._session_maker: sessionmaker | async_sessionmaker | None = None
        self.initiated = False
        self._Base: Type[DeclarativeMeta] = declarative_base(
            metaclass=DeclarativeMeta, cls=ModelBase
        )
        setattr(self._Base, "db", self)
        self.url = url
        self.custom_engine = custom_engine
        self.engine_args = engine_args or {}
        self.session_args = session_args or {}
        self.commit_on_exit = commit_on_exit
        self.session_manager = _session_manager
        self.verbose = verbose
        self.extended = extended
        if async_ and not async_sessionmaker:
            raise SQLAlchemyAsyncioMissing("async_sessionmaker")
        self.async_ = async_
        self.expire_on_commit = expire_on_commit
        self._check_optional_components()

    def init(
        self,
    ) -> None:
        if not self.custom_engine and not self.url:
            raise ValueError("You need to pass a url or a custom_engine parameter.")

        self.engine = self._create_engine()

        self._session_maker = self._make_session_maker()
        self.initiated = True

    def create_all(self):
        print(self.engine)
        if self.async_:
            with self.engine.begin() as conn:
                conn.run_sync(self._Base.metadata.create_all)

        else:
            self._Base.metadata.create_all(self.engine)
        return None

    def print(self, *values):
        if self.verbose >= 3:
            print(*values, flush=True)

    def info(self, *values):
        if self.verbose >= 2:
            print(*values, flush=True)

    def warning(self, message: str):
        if self.verbose >= 1:
            warnings.warn(message)

    def _check_optional_components(self):
        exceptions = []
        if not sqlalchemy_asyncio and self.async_:
            raise SQLAlchemyAsyncioMissing()
        async_classes = [async_sessionmaker, create_async_engine]
        if self.async_:
            for cls in async_classes:
                if not cls:
                    exceptions.append(SQLAlchemyAsyncioMissing(cls.__name__))
        if not self.async_ and all(async_classes):
            self.print(
                "sqlalchemy[asyncio] is installed, to use set async_=True in SQLAlchemy constructor."
            )

        if exceptions:
            raise Exception(*exceptions)

    def _make_session_maker(self) -> Union[sessionmaker, async_sessionmaker]:
        if self.async_ and async_sessionmaker:
            return async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=self.expire_on_commit,
                **self.session_args,
            )
        return sessionmaker(bind=self.engine, **self.session_args)

    def _create_engine(self) -> Union[AsyncEngine, Engine]:
        if self.custom_engine:
            return self.custom_engine
        elif self.async_ and create_async_engine:
            return create_async_engine(self.url, **self.engine_args)
        else:
            return create_engine(self.url, **self.engine_args)

    def __call__(self) -> SQLAlchemy:
        """This is just for compatibility with the old API"""
        if not isinstance(self.session_maker, sessionmaker):
            raise SessionNotInitialisedError
        local_session = self.session_manager(db=self)

        return local_session

    @property
    def session(self) -> Session:
        s = _session.get()
        if not s:
            raise SessionNotInitialisedError
        return _session.get()

    def _make_dialects(self) -> None:
        self.BigInteger = BigInteger()
        self.BigInteger.with_variant()
        return None

    @property
    def session_maker(self) -> Union[sessionmaker, async_sessionmaker]:
        if not self._session_maker:
            raise SessionNotInitialisedError
        return self._session_maker

    @property
    def Base(self) -> Type[ModelBase]:
        return self._Base


class DeclarativeMeta(DeclarativeMeta_):
    db: SQLAlchemy
    session: Session

    def __init__(self, name, bases, attrs):
        for base in bases:
            if hasattr(base, "db"):
                self.db = base.db
                print("set db for ", name)
                break
        super().__init__(name, bases, attrs)

    @property
    def session(self) -> Session:
        return self.db.session

    @property
    def query(self) -> Query:
        return self.db.session.query(self)


db: SQLAlchemy = SQLAlchemy()
