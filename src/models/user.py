import secrets
import string
import urllib.parse
import hashlib
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
from src.config import SECRET_KEY


class User(db.Model):
    __tablename__ = "user"

    id = Column(INTEGER, primary_key=True)
    username = Column(String(32), nullable=False, unique=True, comment="用户名")
    email = Column(String(32), nullable=False, unique=True, comment="email")
    password = Column(String(256), comment="密码")
    is_stuff = Column(TINYINT(1), server_default=text("'0'"), comment="是否是管理人员")
    is_superuser = Column(TINYINT(1), server_default=text("'0'"), comment="是否是超级管理员")
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
    def create(cls, username, password, email):
        pwd = cls.gen_pwd(email, password)
        obj = cls(username=username, password=pwd, email=email)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def paginate(cls, limit=1, offset=0, delete_flag=0):
        paginates = db.session.query(cls).filter_by(delete_flag=delete_flag).order_by(cls.id.desc()).offset(
            offset).limit(limit).all()
        if paginates:
            data = [item.list_to_dict() for item in paginates]
        else:
            data = []
        return data

    @classmethod
    def query_by_username(cls, username):
        result = db.session.query(cls).filter_by(username=username).first()
        return result

    @classmethod
    def query_by_email(cls, email):
        result = db.session.query(cls).filter_by(email=email).first()
        return result

    @classmethod
    def query_by_uname_email(cls, username, email):
        result = db.session.query(cls).filter_by(email=email, username=username).first()
        return result

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "email": self.email,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat(),
            "is_stuff": self.is_stuff,
            "is_superuser": self.is_superuser
        }

    def list_to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }

    @classmethod
    def gen_salt(cls):

        # 字符池：大小写字母 + 数字 + 常用特殊字符（可自定义调整）
        chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
        return ''.join(secrets.choice(chars) for _ in range(10))

    @classmethod
    def gen_pwd(cls, email: str, pwd: str) -> str:
        # 对特殊字符进行 URL 编码（如 & → %26，= → %3D，中文 → %E4%B8%AD）
        encoded_email = urllib.parse.quote(email, safe="")
        encoded_pwd = urllib.parse.quote(pwd, safe="")
        raw_str = f"email={encoded_email}&pwd={encoded_pwd}"
        salted_str = raw_str + SECRET_KEY
        return hashlib.sha256(salted_str.encode("utf-8")).hexdigest()

    def verify_pwd(self, email: str, pwd: str) -> bool:
        pwd = self.gen_pwd(email, pwd)
        return pwd == self.password
