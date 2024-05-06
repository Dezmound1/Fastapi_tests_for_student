from model.auth import User
from fastapi import Depends
from schema.auth import GroupSchema, StudentRead, ByFilterStudentRead
from utils.user_config import current_user
from repositories.operation import (
    OperationGroupRepositiory,
    OperationQuestionRepository,
    OperationStudentRepositiory,
    OperationTestsRepository,
    OperationUserRepositiory,
)
from schema.operation import (
    AddOperationSchema,
    GetStudentByGroup,
    GetTestQwestionsSchema,
    GetTestSchema,
    QuestionSchema,
    QuestionSchemaAdd,
    TestSchemaAdd,
)
from utils.repository import AbstractRepository, SQLAlchemyRepository


class TestService:

    def __init__(self, test_repo: AbstractRepository):
        self.test_repo: AbstractRepository = test_repo()

    async def add_operation_test(self, test: TestSchemaAdd):
        test_dict = test.model_dump()
        test_id = await self.test_repo.add_one(test_dict)
        return test_id


class QuestionService:

    async def add_operation_question(self, question: QuestionSchemaAdd):
        question_dict = question.model_dump()
        question_id = await OperationQuestionRepository().add_one(question_dict)
        return question_id

    async def add_operation_test(
        self,
        tasks: TestSchemaAdd,
        user_id: int,
    ) -> AddOperationSchema:

        tasks_dict = tasks.model_dump()
        tasks_dict["teacher_id"] = user_id
        qwestions = tasks_dict.pop("answers")
        task_id = await OperationTestsRepository().add_one(tasks_dict)
        answer = []
        for qwestion in qwestions:
            qwestion["test_id"] = task_id
            answer.append(await OperationQuestionRepository().add_one(qwestion))
        return AddOperationSchema(task_id=task_id, answer=answer)

    async def get_test(
        self,
        test_id: int,
        user: User,
    ) -> GetTestQwestionsSchema:

        test = await OperationTestsRepository().find_one(test_id)
        qwestions = await OperationQuestionRepository().get_by_filter(**{"test_id":test.id})
        test = GetTestSchema(name=test.name)

        if user.is_superuser == True:
            return GetTestQwestionsSchema(test=test, qwestions=qwestions)
        else:
            student_qwestion = [
                QuestionSchema(id=anser.id, question=anser.question, test_id=anser.test_id) for anser in qwestions
            ]
            return GetTestQwestionsSchema(test=test, qwestions=student_qwestion)


class GroupService:

    async def get_group(
        self,
        user: User,
    ) -> GroupSchema:

        groups = await OperationGroupRepositiory().find_all()
        return groups

    async def get_students_by_group(
        self,
        group_id: int,
        user: User,
    ) -> GetStudentByGroup:
        group = await OperationGroupRepositiory().find_one(group_id)
        students = await OperationStudentRepositiory().get_by_filter(**{"group_id": group.id})
        list_by_filter_student_read = []
        for stud in students:
            user_stud = await OperationUserRepositiory().find_one(id=stud.user_id)
            list_by_filter_student_read.append(
                ByFilterStudentRead(
                    id=stud.id,
                    email=user_stud.email,
                    username=user_stud.username,
                    first_name=stud.first_name,
                    last_name=stud.last_name,
                )
            )
        response = GetStudentByGroup(group=group, student=list_by_filter_student_read)
        return response
