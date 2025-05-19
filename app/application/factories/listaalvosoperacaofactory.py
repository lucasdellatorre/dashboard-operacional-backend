from app.application.usecases.getoperationtargetsusecase import GetOperationTargetsUseCase
from app.domain.services.numeroservice import NumeroService
from app.adapters.repositories.numerorepository import NumeroRepository

class ListaAlvosOperacaoFactory:
    @staticmethod
    def listar() -> GetOperationTargetsUseCase:
        repository = NumeroRepository()
        service = NumeroService(repository)
        return GetOperationTargetsUseCase(service)
