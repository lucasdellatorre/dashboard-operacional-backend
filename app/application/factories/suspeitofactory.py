from app.application.usecases.adicionanumerosuspeitousecase import AdicionaNumeroSuspeitoUseCase
from app.domain.services.numeroservice import NumeroService
from app.application.usecases.atualizarsuspeitousecase import AtualizarSuspeitoUseCase
from app.application.usecases.deletarsuspeitousecase import DeletarSuspeitoUseCase
from app.domain.services.suspeitoservice import SuspeitoService
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.numerorepository import NumeroRepository
from app.application.usecases.getsuspeitobyidusecase import GetSuspeitoByIdUseCase
from app.application.usecases.createsuspeitousecase import CreateSuspeitoUseCase
from app.application.usecases.createemailusecase import CreateEmailUseCase
from app.application.usecases.deleteemailusecase import DeleteEmailUseCase
from app.application.usecases.getallemailusecase import GetAllEmailUseCase 
from app.application.usecases.updateemailusecase import UpdateEmailUseCase

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
    
    @staticmethod
    def delete_email():
        return DeleteEmailUseCase(SuspeitoFactory.build_service())
    
    @staticmethod
    def get_all_email():
        return GetAllEmailUseCase(SuspeitoFactory.build_service())
    
    @staticmethod
    def atualizar_suspeito():
        return AtualizarSuspeitoUseCase(SuspeitoFactory.build_service())
    
    @staticmethod
    def adicionar_telefones():
        num_repo = NumeroRepository()
        num_service = NumeroService(num_repo)
        return AdicionaNumeroSuspeitoUseCase(num_service, SuspeitoFactory.build_service())
    
    @staticmethod
    def delete_suspeito():
        return DeletarSuspeitoUseCase(SuspeitoFactory.build_service())
    
    @staticmethod
    def update_email():
        return UpdateEmailUseCase(SuspeitoFactory.build_service())
