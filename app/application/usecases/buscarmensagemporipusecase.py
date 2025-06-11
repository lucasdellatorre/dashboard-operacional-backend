from typing import List
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.dto.mensagemporipresponsedto import MensagemPorIpResponseDTO
from app.domain.services.targetresolverservice import TargetResolverService

from app.domain.services.mensagemservice import MensagemService

class BuscarMensagemPorIPUseCase:
    def __init__(self, mensagem_service: MensagemService, target_resolver_service: TargetResolverService):
        self.mensagem_service = mensagem_service
        self.target_resolver = target_resolver_service

    def execute(self, filtro: MensagensRequestDTO) -> List[MensagemPorIpResponseDTO]:
        numero_ids, tickets = self.target_resolver.resolver_alvos(filtro)
        
        return self.mensagem_service.obter_quantidade_mensagens_por_ip(
            numeros=numero_ids,
            tickets=tickets,
            tipo=filtro.tipo,
            grupo=filtro.grupo,
            data_inicial=filtro.data_inicial,
            data_final=filtro.data_final,
            hora_inicio=filtro.hora_inicio,
            hora_fim=filtro.hora_fim
        )
