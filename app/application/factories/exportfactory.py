from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository
from app.adapters.repositories.numerorepository import NumeroRepository
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.exportservice import ExportService
from app.application.usecases.exportusecase import ExportUseCase

class ExportFactory:
    @staticmethod
    def export_use_case():
        suspeito_repo = SuspeitoRepository()
        mensagem_repo = MensagemRepository()
        numero_repository = NumeroRepository()

        suspeito_service = SuspeitoService(suspeito_repo, numero_repository)
        mensagem_service = MensagemService(mensagem_repo)
        export_service = ExportService()

        return ExportUseCase(suspeito_service, mensagem_service, export_service)
