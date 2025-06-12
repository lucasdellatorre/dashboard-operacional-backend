from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.exportservice import ExportService

class ExportUseCase:
    def __init__(self, suspeito_service: SuspeitoService, mensagem_service: MensagemService, export_service: ExportService):
        self.suspeito_service = suspeito_service
        self.mensagem_service = mensagem_service
        self.export_service = export_service

    def execute(self, request_dto: MensagensRequestDTO):
        suspeitos = self.suspeito_service.buscar_por_filtro(request_dto)
        mensagens = self.mensagem_service.buscar_por_filtro(request_dto)

        zip_buffer = self.export_service.gerar_csvs(suspeitos, mensagens)
        return zip_buffer
