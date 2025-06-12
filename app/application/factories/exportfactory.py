# app/application/factories/exportfactory.py

from app.adapters.repositories.mensagemrepository import MensagemRepository
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.numerorepository import NumeroRepository
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.exportservice import ExportService

class ExportFactory:
    @staticmethod
    def build_export_service():
        mensagem_repository = MensagemRepository()
        suspeito_repository = SuspeitoRepository()
        numero_repository = NumeroRepository()

        mensagem_service = MensagemService(mensagem_repository)
        suspeito_service = SuspeitoService(suspeito_repository, numero_repository)

        return ExportService(suspeito_service, mensagem_service)
