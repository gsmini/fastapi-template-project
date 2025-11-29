from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    JSON,
    Numeric,
    INTEGER,
    text,
    TEXT
)
from sqlalchemy.dialects.mysql import TINYINT

from src.models import db
from src.libs.logging import logger


class UserFeedbackRecordStatus:
    """
    1创建待审核 2审核通过 3审核拒绝 4回复成功 5回复失败
    """
    Pending = 1
    Approval = 2
    Rejected = 3
    ReplySuccess = 4
    ReplyFail = 5


class UserFeedbackRecord(db.Model):
    __tablename__ = "user_feedback_record"

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, default=0)
    user_email = Column(String(32), nullable=False, comment="用户邮箱")
    title = Column(String(64), nullable=False, comment="标题")
    content = Column(String(256), nullable=False, comment="内容")
    feedback_type = Column(String(64), nullable=False, comment="分类")
    feedback_type_llm = Column(String(64), nullable=False, comment="分类-大模型自动识别的")
    feedback_reply = Column(TEXT, nullable=False, comment="回复模版内容")
    status = Column(TINYINT(1), server_default=text("'0'"), comment="1创建待审核 2审核通过 3审核拒绝 4回复成功 5回复失败")
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

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def query_by_(cls, feedback_type):
        result = db.session.query(cls).filter_by(feedback_type=feedback_type).first()
        return result

    @classmethod
    def query_by_id(cls, ins_id):
        result = db.session.query(cls).filter_by(id=ins_id).first()
        return result

    @classmethod
    def update(cls, ins_id, **kwargs):
        with db.auto_commit():
            obj = db.session.query(cls).filter_by(id=ins_id).update(kwargs)
            return obj

    @classmethod
    def paginate(cls, limit=100, offset=0, delete_flag=0):
        paginates = db.session.query(cls).filter_by(delete_flag=delete_flag).order_by(cls.id.desc()).offset(
            offset).limit(limit).all()
        if paginates:
            data = [item.list_to_dict() for item in paginates]
        else:
            data = []
        return data

    def list_to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "title": self.title,
            "content": self.content,
            "feedback_type": self.feedback_type,
            "feedback_type_llm": self.feedback_type_llm,
            "feedback_reply": self.feedback_reply,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }
