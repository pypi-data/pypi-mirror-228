from __future__ import annotations

from contextlib import ExitStack
from contextvars import ContextVar
from typing import Dict, List, Optional, Union

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import DeclarativeMeta, Session, sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from .exceptions import DBSessionType, MissingSessionError, SessionNotInitialisedError
from .extensions import SQLAlchemy


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        db: Optional[Union[List[SQLAlchemy], SQLAlchemy]],
    ):
        super().__init__(app)
        if not (type(db) == list or type(db) == SQLAlchemy):
            raise DBSessionType()
        if type(db) == SQLAlchemy:
            self.dbs = [db]
        else:
            self.dbs = db
        for db in self.dbs:
            db.create_all()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        with ExitStack() as stack:
            contexts = [stack.enter_context(ctx) for ctx in self.dbs]
            response = await call_next(request)
        return response
