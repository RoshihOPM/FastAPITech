from pydantic import BaseModel
from typing import List, Optional


class ScoreBase(BaseModel):
    student_id: int
    score: int


class ScoreCreate(ScoreBase):
    pass


class ScoreUpdate(BaseModel):
    score: Optional[int] = None


class Score(ScoreBase):
    id: int

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    name: str
    surname: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None


class Student(StudentBase):
    id: int
    scores: List[Score] = []

    class Config:
        orm_mode = True
