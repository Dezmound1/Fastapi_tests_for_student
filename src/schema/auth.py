from typing import Any, Dict, Optional, Type, TypeVar

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

SCHEMA = TypeVar("SCHEMA", bound=BaseModel)

if PYDANTIC_V2:  # pragma: no cover

    def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
        return model.model_dump(*args, **kwargs)  # type: ignore

    def model_validate(schema: Type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
        return schema.model_validate(obj, *args, **kwargs)  # type: ignore

else:  # pragma: no cover  # type: ignore

    def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
        return model.dict(*args, **kwargs)  # type: ignore

    def model_validate(schema: Type[SCHEMA], obj: Any, *args, **kwargs) -> SCHEMA:
        return schema.from_orm(obj)  # type: ignore



class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return model_dump(
            self,   
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})

class UserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    first_name: str
    last_name: str
    group_id: Optional[int | None] = None


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class StudentCreate(BaseModel): 
    id: int
    first_name: str
    last_name: str
    group_id: int
    user_id: int

class StudentInsert(BaseModel):
    first_name: str
    last_name: str
    user_id: int
    group_id: int

class TeacherCreate(BaseModel): 
    id: int
    first_name: str
    last_name: str
    user_id: int

class TeacherInsert(BaseModel):
    first_name: str
    last_name: str
    user_id: int

class GroupSchema(BaseModel):
    id: int
    name: str

