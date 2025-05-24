from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.repositories.interceptacaonumerorepository import IInterceptacaoNumeroRepository
from app.domain.repositories.suspeitorepository import ISuspeitoRepository
from app.adapters.repositories.interceptacaonumerorepository import InterceptacaoNumeroRepository
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.numerorepository import NumeroRepository
from app.application.usecases.getalltargetnumbersusecase import GetAllTargetNumbersUseCase

class ListaAlvosSimplesFactory:
    @staticmethod
    def listar() -> GetAllTargetNumbersUseCase:
        interceptacao_repo: IInterceptacaoNumeroRepository = InterceptacaoNumeroRepository()
        suspeito_repo: ISuspeitoRepository = SuspeitoRepository()
        numero_repo = NumeroRepository()

        interceptacao_service = InterceptacaoNumeroService(interceptacao_repo)
        suspeito_service = SuspeitoService(suspeito_repo, numero_repo) 

        return GetAllTargetNumbersUseCase(interceptacao_service, suspeito_service)
