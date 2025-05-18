from app.application.usecases.suspeitousecase import SuspeitoUseCase
from app.domain.services.suspeitoservice import SuspeitoService
from app.adapters.repositories.suspeitorepository import SuspeitoRepository

class SuspeitoFactory:
    @staticmethod
    def atualizar_suspeito():
        repository = SuspeitoRepository()
        service = SuspeitoService(repository)
        return SuspeitoUseCase(service)
