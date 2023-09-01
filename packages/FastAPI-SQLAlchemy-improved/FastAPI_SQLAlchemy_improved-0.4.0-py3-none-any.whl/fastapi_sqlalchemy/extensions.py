from __future__ import annotations

import asyncio
import logging
import secrets
import warnings
from contextlib import ExitStack
from contextvars import ContextVar, Token
from pprint import pformat, pprint
from typing import Any, Callable, Dict, List, Literal, Optional, Self, Tuple, Type, Union, overload

from curio.meta import from_coroutine
from fastapi import FastAPI
from sqlalchemy import MetaData, create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta as DeclarativeMeta_
from sqlalchemy.orm import Query, Session, declarative_base, sessionmaker
from sqlalchemy.sql import ColumnExpressionArgument
from sqlalchemy.types import BigInteger, Integer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from .exceptions import SessionNotAsync, SessionNotInitialisedError, SQLAlchemyAsyncioMissing
from .types import ModelBase

try:
    import sqlalchemy.ext.asyncio

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

_session = ContextVar("_session", default=None)


class DBSession:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def __enter__(self):
        if not isinstance(self.db.sync_session_maker, sessionmaker):
            raise SessionNotInitialisedError
        session = self.db.sync_session_maker(**self.db.sync_session_args)
        self.token = _session.set(session)

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
        if not isinstance(self.db.async_session_maker, async_sessionmaker):
            raise SessionNotInitialisedError
        session = self.db.async_session_maker(**self.db.async_session_args)
        self.token = _session.set(session)
        return self.db

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.db.session
        try:
            if exc_type is not None:
                await self.db.session.rollback()
            elif self.db.commit_on_exit:
                await self.db.session.commit()
        except:
            await self.db.session.close()
            _session.reset(self.token)


class SQLAlchemy:
    def __init__(
        self,
        url: Optional[URL] = None,
        *,
        async_url: Optional[URL] = None,
        custom_engine: Optional[Engine] = None,
        async_custom_engine: Optional[AsyncEngine] = None,
        engine_args: Dict[str, Any] = None,
        async_engine_args: Dict[str, Any] = None,
        session_args: Dict[str, Any] = None,
        async_session_args: Dict[str, Any] = None,
        commit_on_exit: bool = False,
        verbose: Literal[0, 1, 2, 3] = 0,
        async_: bool = False,
        expire_on_commit: Optional[bool] = False,
        extended: bool = True,
        _session_manager: DBSession = DBSession,
    ):
        self.initiated = False
        self._Base: Type[DeclarativeMeta] = declarative_base(
            metaclass=DeclarativeMeta, cls=ModelBase
        )
        setattr(self._Base, "db", self)
        self.url = url
        self.async_url = async_url
        self.custom_engine = custom_engine
        self.async_custom_engine = async_custom_engine
        self.sync_engine_args = engine_args or {}
        self.async_engine_args = async_engine_args or {}
        self.sync_session_args = session_args or {}
        self.async_session_args = async_session_args or {"expire_on_commit": False}
        self.commit_on_exit = commit_on_exit
        self.session_manager = _session_manager
        self.verbose = verbose
        self.extended = extended
        if async_ and not async_sessionmaker:
            raise SQLAlchemyAsyncioMissing("async_sessionmaker")
        self.async_ = async_
        self.expire_on_commit = expire_on_commit
        self._check_optional_components()
        self._session_maker: sessionmaker = None
        self.sync_engine: Engine = None
        self.async_engine: AsyncEngine = None
        self.sync_session_maker: sessionmaker = None
        self.async_session_maker: async_sessionmaker = None
        if self.url:
            self.init()

    def init(
        self,
    ) -> None:
        if not self.custom_engine and not self.url:
            raise ValueError("You need to pass a url or a custom_engine parameter.")
        if not self.async_custom_engine and not self.async_url and self.async_:
            raise ValueError("You need to pass a async_url or a async_custom_engine parameter.")
        self.sync_engine = self._create_sync_engine()
        self.async_engine = self._create_async_engine()
        self.sync_session_maker = self._make_sync_session_maker()
        self.async_session_maker = self._make_async_session_maker()

        self.initiated = True
        self.metadata = False

    def create_all(self):
        self._Base.metadata.create_all(self.sync_engine)
        self.metadata = True
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

    def _make_sync_session_maker(self) -> sessionmaker:
        return sessionmaker(bind=self.sync_engine, **self.sync_session_args)

    def _make_async_session_maker(self) -> async_sessionmaker:
        if self.async_:
            return async_sessionmaker(bind=self.async_engine, **self.async_session_args)

    def _create_sync_engine(self) -> Union[AsyncEngine, Engine]:
        if self.custom_engine:
            return self.custom_engine
        else:
            return create_engine(self.url, **self.sync_engine_args)

    def _create_async_engine(self) -> AsyncEngine:
        if self.async_:
            if self.async_custom_engine:
                return self.async_custom_engine
            else:
                return create_async_engine(self.async_url, **self.async_engine_args)

    def __call__(self) -> SQLAlchemy:
        """This is just for compatibility with the old API"""
        # if not isinstance(self.sync_session_maker, sessionmaker):
        #     raise SessionNotInitialisedError
        local_session = self.session_manager(db=self)

        return local_session

    @property
    def session(self) -> Union[Session, AsyncSession]:
        s: Union[Session, AsyncSession] = _session.get()
        if not s:
            raise SessionNotInitialisedError
        return s

    @property
    def sync_session(self) -> Session:
        s = self.session
        if self.async_ and type(s) == AsyncSession:
            return s.sync_session
        else:
            raise SessionNotAsync

    def _make_dialects(self) -> None:
        self.BigInteger = BigInteger()
        self.BigInteger.with_variant()
        return None

    # @property
    # def session_maker(self) -> Union[sessionmaker, async_sessionmaker]:
    #     if not self._session_maker:
    #         raise SessionNotInitialisedError
    #     return self._session_maker

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
                break
        super().__init__(name, bases, attrs)

    @property
    def session(self) -> Union[Session, AsyncSession]:
        return self.db.session

    @property
    def query(self) -> Query:
        return self.db.session.query(self)


db: SQLAlchemy = SQLAlchemy()
