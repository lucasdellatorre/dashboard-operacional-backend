from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.application.usecases.getsuspeitobyidusecase import GetSuspeitoByIdUseCase
from app.domain.services.suspeitoservice import SuspeitoService

class SuspeitoFactory:
    @staticmethod
    def get_suspeito_by_id():
        repository = SuspeitoRepository()
        service = SuspeitoService(repository)
        return GetSuspeitoByIdUseCase(service)
