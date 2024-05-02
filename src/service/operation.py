from schema.operation import QuestionSchemaAdd, TestSchemaAdd
from utils.repository import AbstractRepository


class TestService:
    def __init__(self, test_repo: AbstractRepository):
        self.test_repo: AbstractRepository = test_repo()

    async def add_operation_test(self, test: TestSchemaAdd):
        test_dict = test.model_dump()
        test_id = await self.test_repo.add_one(test_dict)
        return test_id


class QuestionService:
    def __init__(self, question_repo: AbstractRepository):
        self.question_repo: AbstractRepository = question_repo()

    async def add_operation_question(self, question: QuestionSchemaAdd):
        question_dict = question.model_dump()
        question_id = await self.question_repo.add_one(question_dict)
        return question_id
