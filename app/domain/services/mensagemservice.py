from collections import defaultdict
from app.domain.repositories.mensagemrepository import IMensagemRepository
from app.domain.entities.numero import Numero

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