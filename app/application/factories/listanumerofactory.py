from app.application.usecases.getallnumbersusecase import GetAllNumbersUseCase
from app.domain.services.numeroservice import NumeroService
from app.adapters.repositories.numerorepository import NumeroRepository

class ListaNumerosFactory:
    @staticmethod
    def listar() -> GetAllNumbersUseCase:
        repository = NumeroRepository()
        service = NumeroService(repository)
        return GetAllNumbersUseCase(service)
