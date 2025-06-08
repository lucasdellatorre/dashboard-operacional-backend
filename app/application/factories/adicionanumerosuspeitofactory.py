from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.application.usecases.adicionanumerosuspeitousecase import AdicionaNumeroSuspeitoUseCase
from app.domain.services.numeroservice import NumeroService
from app.adapters.repositories.numerorepository import NumeroRepository
from app.domain.services.suspeitoservice import SuspeitoService

class AdicionaNumeroSuspeitoFactory:
    @staticmethod
    def criar() -> AdicionaNumeroSuspeitoUseCase:
        num_repository = NumeroRepository()
        sus_repository = SuspeitoRepository()
        num_service = NumeroService(num_repository)
        suspeito_service = SuspeitoService(sus_repository, num_repository)
        return AdicionaNumeroSuspeitoUseCase(num_service, suspeito_service)