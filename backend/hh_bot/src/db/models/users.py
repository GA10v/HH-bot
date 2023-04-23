from models.base import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Text


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Text, unique=True)
    is_super = Column(Boolean, default=False)


class View(BaseModel):
    __tablename__ = 'views'

    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    link = Column(ForeignKey('vacancies.link'), nullable=False)


class Like(BaseModel):
    __tablename__ = 'likes'

    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    link = Column(ForeignKey('vacancies.link'), nullable=False)
    is_send = Column(Boolean, default=False)
