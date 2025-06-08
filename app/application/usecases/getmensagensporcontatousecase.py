from typing import List, Dict
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService
from app.domain.services.interceptacaoservice import InterceptacaoService
from app.domain.services.suspeitoservice import SuspeitoService

class GetMensagensPorContatoUseCase:
    def __init__(
        self,
        suspeito_service: SuspeitoService,
        interceptacao_service: InterceptacaoService,
        interceptacao_numero_service: InterceptacaoNumeroService,
        mensagens_service: MensagemService
    ):
        self.suspeito_service = suspeito_service
        self.interceptacao_service = interceptacao_service
        self.interceptacao_numero_service = interceptacao_numero_service
        self.mensagens_service = mensagens_service

    def execute(self, filtros: MensagensRequestDTO) -> List[Dict]:
        """
        Executa a lógica de retorno da quantidade de mensagens por contato
        com base nos filtros recebidos.
        """
        if not (filtros.suspeitos or filtros.numeros or filtros.operacoes):
            raise ValueError("É necessário informar ao menos um dos seguintes: suspeitos, números ou operações.")

        numero_ids = set()

        # 1. Se houver suspeitos, buscar os números vinculados a eles
        if filtros.suspeitos:
            numeros_dos_suspeitos = self.suspeito_service.get_numeros_by_suspeito_ids(filtros.suspeitos)
            numero_ids.update([n['numero'] for n in numeros_dos_suspeitos])

        # 2. Adicionar números fornecidos diretamente
        if filtros.numeros:
            numero_ids.update(filtros.numeros)

        # Busca tickets das operações sempre,
        # mas só carrega números via tickets se nenhum número ou suspeito foi fornecido
        if filtros.operacoes:
            interceptacoes = self.interceptacao_service.get_interceptacoes_por_operacoes(filtros.operacoes)
            tickets = [i.internalTicketNumber for i in interceptacoes]
            ticketsIds = [i.id for i in interceptacoes]
            
            if not numero_ids:
                numeros_por_ticket = self.interceptacao_numero_service.get_alvos_por_interceptacoes(ticketsIds)
                numero_ids.update([n['numero'] for n in numeros_por_ticket])

        if not numero_ids:
            raise ValueError("Nenhum número encontrado com base nos filtros fornecidos.")

        numero_ids_str = [str(n) for n in numero_ids]

        return self.mensagens_service.obter_quantidade_mensagens_por_contato(
            numeros=numero_ids_str,
            tickets=tickets,
            tipo=filtros.tipo,
            grupo=filtros.grupo,
            data_inicial=filtros.data_inicial,
            data_final=filtros.data_final,
            hora_inicio=filtros.hora_inicio,
            hora_fim=filtros.hora_fim
        )