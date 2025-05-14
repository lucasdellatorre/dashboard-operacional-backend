from ..repositories.testrepository import TestRepository

class TestService():
    def __init__(self, todo_repository: TestRepository):
        self.todo_repository = todo_repository
        
    def say_hi(self) -> str:
        return self.todo_repository.say_hi()