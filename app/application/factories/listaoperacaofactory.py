from app.adapters.repositories.numerorepository import NumeroRepository
from app.application.usecases.listaoperacaousercase import ListarOperacoesUseCase
from app.domain.services.numeroservice import NumeroService

class ListaOperacaoFactory:
    @staticmethod
    def listar_operacoes():
        repository = NumeroRepository()
        service = NumeroService(repository)
        return ListarOperacoesUseCase(service)
