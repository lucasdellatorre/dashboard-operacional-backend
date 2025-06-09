from typing import List
from app.application.dto.mensagempordiaresponsedto import MensagemPorDiaResponseDTO
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.targetresolverservice import TargetResolverService

class BuscarMensagemPorDiaUseCase:
    def __init__(self, target_resolver_service: TargetResolverService, mensagem_service: MensagemService):
        self.mensagem_service = mensagem_service
        self.target_resolver = target_resolver_service

    def execute(self, filtro: MensagensRequestDTO) -> List[MensagemPorDiaResponseDTO]:
        numero_ids, tickets = self.target_resolver.resolver_alvos(filtro)
        
        return self.mensagem_service.obter_quantidade_mensagens_por_dia(
            numeros=numero_ids,
            tickets=tickets,
            tipo=filtro.tipo,
            grupo=filtro.grupo,
            data_inicial=filtro.data_inicial,
            data_final=filtro.data_final,
            hora_inicio=filtro.hora_inicio,
            hora_fim=filtro.hora_fim
        )
