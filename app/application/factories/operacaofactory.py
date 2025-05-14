from app.adapters.repositories.operacaorepository import OperacaoRepository
from app.application.usecases.getalloperacaousecase import GetAllOperacaoUseCase
from app.application.usecases.createoperacaousecase import CreateOperacaoUseCase
from app.domain.services.operacaoservice import OperacaoService

class OperacaoFactory:
    @staticmethod
    def get_all_operacao():
        operacao_repository = OperacaoRepository()
        operacao_service = OperacaoService(operacao_repository)
        return GetAllOperacaoUseCase(operacao_service)
    
    @staticmethod
    def create_operacao():
        operacao_repository = OperacaoRepository()
        operacao_service = OperacaoService(operacao_repository)
        return CreateOperacaoUseCase(operacao_service)
    
    
