# -*- coding:utf-8 -*-
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_POOL_SIZE,
    SQLALCHEMY_POOL_RECYCLE,
    SQLALCHEMY_POOL_TIMEOUT,
)


class _SQLAlchemy:
    def __init__(self):
        self.Model = declarative_base()
        self.session = self.get_session_factory()

    @staticmethod
    def get_engine():
        return create_engine(
            SQLALCHEMY_DATABASE_URI,
            pool_size=SQLALCHEMY_POOL_SIZE,
            pool_recycle=SQLALCHEMY_POOL_RECYCLE,
            pool_timeout=SQLALCHEMY_POOL_TIMEOUT,
        )

    def get_session_factory(self):
        session_factory = sessionmaker(bind=self.get_engine())
        return scoped_session(session_factory)

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        else:
            self.session.remove()


db = _SQLAlchemy()
