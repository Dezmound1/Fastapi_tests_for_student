from src.model.auth import Group, Student, Teacher, User
from src.model.operation import Answer, Tests, Question
from src.utils.repository import SQLAlchemyRepository


class OperationTestsRepository(SQLAlchemyRepository):
    model = Tests
    

class OperationQuestionRepository(SQLAlchemyRepository):
    model = Question

class OperationTeacherRepository(SQLAlchemyRepository):
    model = Teacher

class OperationGroupRepositiory(SQLAlchemyRepository):
    model = Group

class OperationStudentRepositiory(SQLAlchemyRepository):
    model = Student

class OperationUserRepositiory(SQLAlchemyRepository):
    model = User

class OperationAnswerRepositiory(SQLAlchemyRepository):
    model = Answer