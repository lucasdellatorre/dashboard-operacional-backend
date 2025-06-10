from typing import List, Dict
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.targetresolverservice import TargetResolverService

class GetMensagensPorContatoUseCase:
    def __init__(
        self,
        target_resolver_service: TargetResolverService,
        mensagens_service: MensagemService
    ):
        self.target_resolver = target_resolver_service
        self.mensagens_service = mensagens_service

    def execute(self, filtros: MensagensRequestDTO) -> List[Dict]:
        numero_ids, tickets = self.target_resolver.resolver_alvos(filtros)

        return self.mensagens_service.obter_quantidade_mensagens_por_contato(
            numeros=numero_ids,
            tickets=tickets,
            tipo=filtros.tipo,
            grupo=filtros.grupo,
            data_inicial=filtros.data_inicial,
            data_final=filtros.data_final,
            hora_inicio=filtros.hora_inicio,
            hora_fim=filtros.hora_fim
        )
