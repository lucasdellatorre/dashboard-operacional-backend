from app.domain.services.suspeitoservice import SuspeitoService
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.numerorepository import NumeroRepository
from app.application.usecases.getsuspeitobyidusecase import GetSuspeitoByIdUseCase
from app.application.usecases.createsuspeitousecase import CreateSuspeitoUseCase
from app.application.usecases.createemailusecase import CreateEmailUseCase

class SuspeitoFactory:
    @staticmethod
    def build_service():
        return SuspeitoService(
            suspeito_repository=SuspeitoRepository(),
            numero_repository=NumeroRepository()
        )

    @staticmethod
    def get_suspeito_by_id():
        return GetSuspeitoByIdUseCase(SuspeitoFactory.build_service())

    @staticmethod
    def create_suspeito():
        return CreateSuspeitoUseCase(SuspeitoFactory.build_service())
    
    @staticmethod
    def create_email():
        return CreateEmailUseCase(SuspeitoFactory.build_service())