from __future__ import annotations
from pydantic import BaseModel


class TestSchema(BaseModel):
    id: int
    name: str
    stud_id: int
    teacher_id: int
    answers: list[QuestionSchema]


class QuestionSchema(BaseModel):
    id: int
    question: str
    answer: str
    test: int


class TestSchemaAdd(BaseModel):
    name: str
    stud_id: int
    teacher_id: int

class QuestionSchemaAdd(BaseModel):
    question: str
    answer: str
    test_id: int