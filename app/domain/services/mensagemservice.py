from collections import defaultdict
from app.domain.repositories.mensagemrepository import IMensagemRepository
from app.domain.entities.numero import Numero
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from typing import List, Dict

class MensagemService():
    def __init__(self, mensagem_repository: IMensagemRepository):
        self.repository = mensagem_repository
        
    def count_mensagens_por_alvo(self, numero: Numero) -> dict[str, int]:
        mensagens = self.repository.get_mensagens_from_numero_id(numero.id)
        mem = defaultdict(int)
        
        for mensagem in mensagens:
            numero_alvo = numero.numero
            remetente = mensagem.remetente
            destinatario = mensagem.destinatario
            
            if remetente == numero_alvo:
                mem[destinatario] += 1
            elif destinatario == numero_alvo:
                mem[remetente] += 1
                
        return dict(mem)    
    
    def obter_quantidade_mensagens_por_contato(
        self,
        request: Dict
    ) -> List[Dict]:
        """
        Orquestra a busca pela quantidade de mensagens por contato.

        1. Recebe a requisição validada.
        2. Extrai os IDs dos números.
        3. Chama o método do repositório para buscar os dados no banco.
        4. Retorna o resultado.
        """
        # A validação dos dados da requisição (se numero_ids existe, etc.)
        # é feita automaticamente pelo Pydantic antes mesmo de chegar aqui.

        # Chama o método do repositório, passando apenas os dados necessários.
        resultados = self.repository.contar_mensagens_por_contato(
            numero_ids=request
        )

        return resultados