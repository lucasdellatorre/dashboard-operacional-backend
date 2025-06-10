from typing import List
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.entities.mensagem import Mensagem
from app.application.dto.mensagemporipresponsedto import MensagemPorIpResponseDTO
from app.domain.services.ipmensagemservice import IpmensagemService
from app.application.dto.filtromensagemdto import FiltroMensagemDTO
from app.domain.services.targetresolverservice import TargetResolverService

class BuscarMensagemPorIPUseCase:
    def __init__(self, ipmensagem_service: IpmensagemService, target_resolver_service=TargetResolverService):
        self.target_resolver = target_resolver_service
        self.ipmensagem_service = ipmensagem_service

    def execute(self, filtro: MensagensRequestDTO) -> List[MensagemPorIpResponseDTO]:
        numero_ids, tickets = self.target_resolver.resolver_alvos(filtro)
        filtro.numeros = numero_ids

        return self.ipmensagem_service.buscar_mensagens_por_ip(filtro , tickets)
