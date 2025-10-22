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

    create_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )
    update_time = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="更新时间",
    )

    """
    with db.auto_commit():会报错
    所以改成手动commit
    Instance <User at 0x10c35e660> is not bound to a Session; attribute refresh operation cannot proceed (Background on this error at: https://sqlalche.me/e/14/bhk3)
    """

    @classmethod
    def create(cls, username, password):
        obj = cls(username=username, password=password)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def paginate(cls, limit=1, offset=100):
        paginates = db.session.query(cls).order_by(cls.id.desc()).offset(offset).limit(limit).all()
        if paginates:
            data = [item.list_to_dict() for item in paginates]
        else:
            data = []
        return data

    @classmethod
    def query_by_username(cls, username):
        result = db.session.query(cls).filter_by(username=username).first()

        return result

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }

    def list_to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }
