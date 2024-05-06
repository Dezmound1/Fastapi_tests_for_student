from fastapi import APIRouter, Depends

from model.auth import User
from repositories.operation import OperationQuestionRepository, OperationTeacherRepository, OperationTestsRepository
from schema.auth import StudentRead
from schema.operation import AddOperationSchema, GetStudentByGroup, TestSchema, TestSchemaAdd
from service.operation import GroupService, QuestionService
from utils.user_config import current_user, current_user_not_superuser


router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


# Поинты преподавателей
@router.get("/get_groups")  # получение списка групп доступно только преподавателем
async def get_groups(
    user: User = Depends(current_user),
):
    response = await GroupService().get_group(user=user)
    return response


@router.get("/get_students_by_group") # получение информации о студентах по группе
async def get_student(
    group_id: int,
    user: User = Depends(current_user),
) -> GetStudentByGroup:  
    response = await GroupService().get_students_by_group(group_id=group_id, user=user)
    print(response)
    return response


@router.post("/add_test")  # добавление нового теста, тесты добавляют только преподаватели
async def add_test(
    tasks: TestSchemaAdd,
    user: User = Depends(current_user),
) -> AddOperationSchema:

    response = await QuestionService(OperationQuestionRepository).add_operation_test(tasks=tasks, user_id=user.id)
    return response


@router.get("/get_test")
async def get_test_by_student(
    test_id: int,
    user: User = Depends(current_user_not_superuser),
):  # получение всех тестов студентом, может получить только те тесты, на которые он записан
    response = await QuestionService().get_test(test_id=test_id, user=user)
    return response


# Поинты студентов
@router.get("/get_question_by_test")
async def get_question_by_test(
    student_id: int, test_id: int
):  # получение вопросов студентом по тесту, на который он записан
    pass


@router.post("/add_answer")
async def add_answer(
    student_id: int, test_id: int, answer: str
):  # внесение ответа по тесту студентом, на который он записан
    pass
