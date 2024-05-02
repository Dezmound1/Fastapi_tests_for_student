from model.operation import Tests, Question
from utils.repository import SQLAlchemyRepository


class OperationTestsRepository(SQLAlchemyRepository):
    model = Tests

class OperationQuestionRepository(SQLAlchemyRepository):
    model = Question
