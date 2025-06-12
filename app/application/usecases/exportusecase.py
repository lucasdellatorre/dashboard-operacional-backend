from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.exportservice import ExportService
from app.domain.services.targetresolverservice import TargetResolverService


class ExportUseCase:
    def __init__(self, target_resolver_service: TargetResolverService, suspeito_service: SuspeitoService, mensagem_service: MensagemService, export_service: ExportService):
        self.suspeito_service = suspeito_service
        self.mensagem_service = mensagem_service
        self.export_service = export_service
        self.target_resolver = target_resolver_service


    def execute(self, request_dto: MensagensRequestDTO):
        numero_ids, tickets = self.target_resolver.resolver_alvos(request_dto)
        suspeitos = self.suspeito_service.buscar_por_filtro(request_dto)
        mensagens = self.mensagem_service.buscar_por_filtro(numeros=numero_ids,
                                                            tickets=tickets,
                                                            tipo=request_dto.tipo,
                                                            grupo=request_dto.grupo,
                                                            data_inicial=request_dto.data_inicial,
                                                            data_final=request_dto.data_final,
                                                            hora_inicio=request_dto.hora_inicio,
                                                            hora_fim=request_dto.hora_fim)

        zip_buffer = self.export_service.gerar_csvs(suspeitos, mensagens)
        return zip_buffer
