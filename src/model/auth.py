from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.pg import Base
from schema.auth import GroupSchema


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    registered_at: Mapped[int] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    hashed_password: Mapped[str] = Column(String(length=1024))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)


class Group(Base):
    __tablename__ = "student_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    def to_read_model(self) -> GroupSchema:
        return GroupSchema(
            id=self.id,
            name=self.name,
        )


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    group_id: Mapped[int] = mapped_column(ForeignKey("student_group.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
