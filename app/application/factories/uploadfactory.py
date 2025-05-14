from app.adapters.repositories.operacaorepository import OperacaoRepository
from app.adapters.repositories.planilharepository import PlanilhaRepository
from app.application.usecases.interceptacaouploadusecase import InterceptacaoUploadUseCase
from app.domain.services.operacaoservice import OperacaoService
from app.domain.services.uploadservice import UploadService

class UploadInterceptacaoFactory:
    @staticmethod
    def create():
        planilha_repository = PlanilhaRepository()
        operacao_repository = OperacaoRepository()
        upload_service = UploadService(planilha_repository)
        operacao_service = OperacaoService(operacao_repository)
        return InterceptacaoUploadUseCase(upload_service, operacao_service)