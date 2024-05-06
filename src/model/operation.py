from __future__ import annotations

from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.pg import Base
from schema.operation import QuestionSchema, TestSchema


class Tests(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))

    def to_read_model(self) -> TestSchema:
        return TestSchema(
            id=self.id,
            name=self.name,
            teacher_id=self.teacher_id,
        )


class StudentTest(Base):
    __tablename__ = "tests_tudent"

    test_student_id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(255))
    answer: Mapped[str] = mapped_column(String(255))
    test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))

    def to_read_model(self) -> QuestionSchema:
        return QuestionSchema(
            id=self.id,
            question=self.question,
            answer=self.answer,
            test_id=self.test_id,
        )
