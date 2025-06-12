from typing import Tuple, List
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.dto.teiaipmessagecountdto import TeiaIPMessageCountRequestDTO
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.interceptacaoservice import InterceptacaoService
from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService

class TargetResolverService:
    def __init__(self, suspeito_service, interceptacao_service, interceptacao_numero_service):
        self.suspeito_service: SuspeitoService = suspeito_service
        self.interceptacao_service: InterceptacaoService = interceptacao_service
        self.interceptacao_numero_service: InterceptacaoNumeroService = interceptacao_numero_service
    def resolver_alvos(self, filtros: MensagensRequestDTO) -> Tuple[List[str], List[str]]:
        if not (filtros.suspeitos or filtros.numeros or filtros.operacoes):
            raise ValueError("É necessário informar ao menos um dos seguintes: suspeitos, números ou operações.")

        numero_ids = set()
        tickets = []

        if filtros.suspeitos:
            numeros_dos_suspeitos = self.suspeito_service.get_numeros_by_suspeito_ids(filtros.suspeitos)
            numero_ids.update([n['numero'] for n in numeros_dos_suspeitos])

        if filtros.numeros:
            numero_ids.update(filtros.numeros)

        if filtros.operacoes:
            interceptacoes = self.interceptacao_service.get_interceptacoes_por_operacoes(filtros.operacoes)
            tickets = [i.internalTicketNumber for i in interceptacoes]
            tickets_ids = [i.id for i in interceptacoes]

            if not numero_ids:
                numeros_por_ticket = self.interceptacao_numero_service.get_alvos_por_interceptacoes(tickets_ids)
                numero_ids.update([n['numero'] for n in numeros_por_ticket])

        if not numero_ids:
            raise ValueError("Nenhum número encontrado com base nos filtros fornecidos.")

        numero_ids_str = [str(n) for n in numero_ids]
        return numero_ids_str, tickets
