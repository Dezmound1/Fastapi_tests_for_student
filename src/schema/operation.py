from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

from schema.auth import ByFilterStudentRead, GroupSchema, StudentRead


class TestSchema(BaseModel):
    id: int
    name: str
    teacher_id: int

class QuestionSchema(BaseModel):
    id: int
    question: str
    answer: str = None
    test_id: int

class TestSchemaAdd(BaseModel):
    name: str
    answers: list[QuestionSchema]

class QuestionSchemaAdd(BaseModel):
    question: str
    answer: str
    test_id: int

class AddOperationSchema(BaseModel):
    task_id: int
    answer: list[int]

class GetTestSchema(BaseModel):
    name: str

class GetTestQwestionsSchema(BaseModel):
    test: GetTestSchema
    qwestions: List[QuestionSchema]

class GetStudentByGroup(BaseModel):
    group: GroupSchema
    student: List[ByFilterStudentRead]