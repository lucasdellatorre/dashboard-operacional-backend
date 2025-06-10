from app.application.dto.numeromessagecountdto import NumeroMessageCountRequestDTO, NumeroMessageCountResponseDTO
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.numeroservice import NumeroService
from app.domain.entities.numero import Numero


class TeiaMessageCountUseCase:
    def __init__(self, numero_service: NumeroService, mensagem_service: MensagemService):
        self.numero_service = numero_service
        self.mensagem_service = mensagem_service

    def execute(self, request: NumeroMessageCountRequestDTO) -> NumeroMessageCountResponseDTO:
        numeros_ids = request.numeros
        nodes = []
        links = []
        RED = 3
        GRAY = 7
        
        for id in numeros_ids:
            numero: Numero = self.numero_service.find(id)
            numero_telefone = numero.numero
            
            is_alvo = self.numero_service.isAlvo(id)
            
            nodes.append(node)
            
            if not is_alvo: continue
            
            relations: dict[str, int] = self.mensagem_service.count_mensagens_por_alvo(numero)
            
            for target, value in relations.items():
                links.append({ "source": numero_telefone, "target": target, "value": value })
                
        return NumeroMessageCountResponseDTO(nodes, links)