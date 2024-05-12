from typing import Generic, Optional
from pydantic import BaseModel

from fastapi import Depends, HTTPException, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models
from sqlalchemy import insert
from sqlalchemy.future import select

from src.db.pg import async_session_maker
from conf import SECRET_AUTH
from src.model.auth import Student, Teacher, User, Group
from src.schema.auth import StudentInsert, TeacherInsert, UserCreate
from src.utils.auth import get_user_db


class UserManager(Generic[models.UP, models.ID], IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_login(self, user: User, request: Optional[Request] = None, response: Optional[Response] = None):
        print(f"User {user.id} logged in.")

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = user_create.create_update_dict_superuser() if not safe else user_create.create_update_dict()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        # Транзакцию

        if user_create.group_id:
            async with async_session_maker() as session:
                # Выполняем запрос к базе данных
                result = await session.execute(select(Group).where(Group.id == user_create.group_id))
                group = result.scalars().first()

                if not group:
                    raise HTTPException(status_code=400, detail="Group not found")

        user_dict_fastapi = user_dict.copy()
        user_dict_fastapi.pop("first_name", None)
        user_dict_fastapi.pop("last_name", None)
        user_dict_fastapi.pop("group_id", None)

        created_user = await self.user_db.create(user_dict_fastapi)
        await self.on_after_register(created_user, request)

        if user_create.is_superuser or user_create.group_id == 0: # преподаватель не имеет группы, либо он имеет статус суперпользователя
            teacher = TeacherInsert(
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                user_id=created_user.id,
            )
            await self.insert_user_db(Teacher, teacher)
        else:
            student = StudentInsert(
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                group_id=user_create.group_id,
                user_id=created_user.id,
            )
            await self.insert_user_db(Student, student)
        return created_user

    async def insert_user_db(self, table, model: BaseModel):
        try:
            async with async_session_maker() as session:
                stmt = insert(table).values(**model.model_dump())
                await session.execute(stmt)
                await session.commit()
                return {"status": "транзакция прошла успешно"}
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "details": "Ошибка вставки",
                },
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
