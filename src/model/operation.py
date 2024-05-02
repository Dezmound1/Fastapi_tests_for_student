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
    stud_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    answers: Mapped[List[Question]] = relationship(back_populates="tests")

    def to_read_model(self) -> TestSchema:
        return TestSchema(
            id=self.id,
            name=self.name,
            stud_id=self.stud_id,
            teacher_id=self.teacher_id,
            answers=self.answers,
        )


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(255))
    answer: Mapped[str] = mapped_column(String(255))
    test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))
    test: Mapped["Tests"] = relationship(back_populates="question")

    def to_read_model(self) -> QuestionSchema:
        return QuestionSchema(
            id=self.id,
            question=self.question,
            answer=self.answer,
            test=self.test,
        )
