from pydantic import BaseModel


class Vacancy(BaseModel):
    name: str
    link: str
    company: str
    area: str
    experience: str
    salary: str
    skills: str
    timestamp: str
