from sqlalchemy import Column, DateTime, Text
from models.base import BaseModel


class Vacancy(BaseModel):
    __tablename__ = 'vacancies'

    name = Column(Text, nullable=True)
    link = Column(Text, nullable=True, unique=True)
    company = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    salary = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=True)
