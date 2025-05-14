from app.adapters.repositories.testrepositorymemory import TestRepositoryMemory
from app.application.usecases.sayhiusecase import SayHiUseCase
from app.domain.services.testservice import TestService

class TestFactory:
    @staticmethod
    def create_say_hi_use_case():
        test_repository = TestRepositoryMemory()
        test_service = TestService(test_repository)
        return SayHiUseCase(test_service)