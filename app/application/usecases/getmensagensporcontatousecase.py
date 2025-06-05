from typing import List, Dict
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService

class GetMensagensPorContatoUseCase:
    def __init__(self, mensagens_service: MensagemService):
        self.mensagens_service = mensagens_service

    def execute(self, filtros: MensagensRequestDTO) -> List[Dict]:
        """
        Executa a lógica de retorno da quantidade de mensagens por contato
        com base nos filtros recebidos.
        """
        if not filtros.operacoes:
            raise ValueError("É necessário informar ao menos uma operação.")
        
        numeros_obj = InterceptacaoNumeroService.get_all_numeros()
    
        # 2. Extrai apenas os IDs dos objetos para uma nova lista.
        ids_dos_numeros = [n.id for n in numeros_obj]
        
        # 3. Atualiza o DTO de filtros com a lista de IDs obtida.
        #    Isso garante que o serviço de mensagens buscará por TODOS os números.
        numero_ids = ids_dos_numeros    
        
        return self.mensagens_service.obter_quantidade_mensagens_por_contato(numero_ids)
