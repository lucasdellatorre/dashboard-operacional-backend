from app.adapters.repositories.numerorepository import NumeroRepository
from app.application.usecases.listanumerousercase import ListarNumeroUseCase
from app.domain.services.numeroservice import NumeroService

class ListaNumeroFactory:
    @staticmethod
    def listar_numero():
        repository = NumeroRepository()
        service = NumeroService(repository)
        return ListarNumeroUseCase(service)
