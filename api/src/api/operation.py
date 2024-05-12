from fastapi import APIRouter, Depends

from src.model.auth import User
from src.schema.operation import AddAnswerOnQuwestionSchema, AddOperationSchema, AnswerSchema, GetStudentByGroup, GetTestQwestionsSchema, TestSchemaAdd
from src.service.operation import AddAnswerService, GroupService, QuestionService
from src.utils.user_config import current_user, current_user_not_superuser


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


@router.get("/get_students_by_group")  # получение информации о студентах по группе
async def get_student(
    group_id: int,
    user: User = Depends(current_user),
) -> GetStudentByGroup:
    response = await GroupService().get_students_by_group(group_id=group_id)
    print(response)
    return response


@router.post("/add_test")  # добавление нового теста, тесты добавляют только преподаватели
async def add_test(
    tasks: TestSchemaAdd,
    user: User = Depends(current_user),
) -> AddOperationSchema:

    stmt = await QuestionService().add_operation_test(tasks=tasks, user_id=user.id)
    return stmt


@router.get("/get_test")  # получение всех тестов студентом, может получить только те тесты, на которые он записан
async def get_test_by_student(
    test_id: int,
    user: User = Depends(current_user_not_superuser),
):
    response = await QuestionService().get_test(test_id=test_id, user=user)
    return response


# Поинты студентов
@router.get("/get_questions_by_test")  # получение вопросов студентом по тесту, на который он записан
async def get_question_by_test(
    test_id: int,
    user: User = Depends(current_user_not_superuser),
) -> GetTestQwestionsSchema:
    response = await QuestionService().get_test(test_id=test_id, user=user)
    return response


@router.post("/add_answer")  # внесение ответа по тесту студентом, на который он записан
async def add_answer(
    answer: AnswerSchema,
    user: User = Depends(current_user_not_superuser),
) -> AddAnswerOnQuwestionSchema:
    stmt = await AddAnswerService().add_answer(answer=answer, user=user.id)
    return stmt 
