from app.domain.services.testservice import TestService

class SayHiUseCase:
    def __init__(self, test_service: TestService):
        self.test_service = test_service

    def execute(self):
        return self.test_service.say_hi()