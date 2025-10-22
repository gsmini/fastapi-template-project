from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    JSON,
    Numeric,
    INTEGER,
    text,
)
from sqlalchemy.dialects.mysql import TINYINT

from src.models import db


class User(db.Model):
    __tablename__ = "user"

    id = Column(INTEGER, primary_key=True)
    username = Column(String(32), nullable=False, unique=True, comment="用户名")
    password = Column(String(32), comment="密码")
    delete_flag = Column(TINYINT(1), server_default=text("'0'"), comment="是否删除")

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="更新时间",
    )

    @classmethod
    def create(cls, username, password):
        obj = cls(username=username, password=password)
        with db.auto_commit():
            db.session.add(obj)
        return obj

    @classmethod
    def query_by_username(cls, username):
        result = db.session.query(cls).filter_by(username=username).first()
        return result

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "create_time": self.created_at,
            "update_time": self.updated_at
        }
