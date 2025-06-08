from app.application.usecases.adicionanumerosuspeitousecase import AdicionaNumeroSuspeitoUseCase
from app.domain.services.numeroservice import NumeroService
from app.adapters.repositories.numerorepository import NumeroRepository

class AdicionaNumeroSuspeitoFactory:
    @staticmethod
    def criar() -> AdicionaNumeroSuspeitoUseCase:
        repository = NumeroRepository()
        service = NumeroService(repository)
        return AdicionaNumeroSuspeitoUseCase(service)