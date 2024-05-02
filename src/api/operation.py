
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)

# Поинты преподавателей
@router.get("/get_tests_by_teacher")
async def get_tests(teacher_id: int): # получение всех тестов учителем, может получить только те тесты, которые он создал

    pass

@router.get("/get_groups")
async def get_groups(teacher_id: int): # получение списка групп доступно только преподавателем
    pass

@router.get("/get_student")
async def get_student(teacher_id: int, student_id: int): # получение информации о студенте для назначения теста
    pass

@router.post("/add_test")
async def add_test(teacher_id: int): # добавление нового теста, тесты добавляют только преподаватели
    
    pass

@router.post("/add_question")
async def add_question(teacher_id: int, test_id: int): # добавление вопроса для теста преподавателем
    pass



# Поинты студентов
@router.get("/get_tests_by_student")
async def get_test_by_student(student_id: int): # получение всех тестов студентом, может получить только те тесты, на которые он записан
    pass

@router.get("/get_question_by_test")
async def get_question_by_test(student_id: int, test_id: int): # получение вопросов студентом по тесту, на который он записан
    pass

@router.post("/add_answer")
async def add_answer(student_id: int, test_id:int, answer: str): # внесение ответа по тесту студентом, на который он записан
    pass
