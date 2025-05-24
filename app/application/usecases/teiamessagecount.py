from app.application.dto.numeromessagecountdto import NumeroMessageCountRequestDTO, NumeroMessageCountResponseDTO
from app.domain.entities.numerosuspeito import NumeroSuspeito
from app.domain.entities.suspeito import Suspeito
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.numeroservice import NumeroService
from app.domain.entities.numero import Numero
from app.domain.services.suspeitoservice import SuspeitoService


class TeiaMessageCountUseCase:
    ALVO = 5
    INTERLOCUTOR = 6
    SUSPEITO = 7

    def __init__(
        self,
        numero_service: NumeroService,
        mensagem_service: MensagemService,
        suspeito_service: SuspeitoService
    ):
        self.numero_service = numero_service
        self.mensagem_service = mensagem_service
        self.suspeito_service = suspeito_service

    def execute(self, request: NumeroMessageCountRequestDTO) -> NumeroMessageCountResponseDTO:
        nodes = []
        links = []

        for numero_id in request.targetId:
            self._process_target(numero_id, request.operationId, nodes, links)

        for suspeito_id in request.suspectId:
            self._process_suspect(suspeito_id, request.operationId, nodes, links)

        return NumeroMessageCountResponseDTO(nodes, links)

    def _process_target(self, numero_id: int, operation_ids: list[int], nodes: list, links: list):
        if not self.numero_service.numeroIsOnOperation(numero_id, operation_ids):
            return

        numero = self.numero_service.find(numero_id)
        telefone = numero.numero
        is_alvo = self.numero_service.isAlvo(numero_id)

        group = self.ALVO if is_alvo else self.INTERLOCUTOR
        nodes.append({"id": telefone, "group": group})

        if not is_alvo:
            return

        relations = self.mensagem_service.count_mensagens_por_alvo(numero)
        for target, value in relations.items():
            links.append({"source": telefone, "target": target, "value": value})

    def _process_suspect(self, suspeito_id: int, operation_ids: list[int], nodes: list, links: list):
        suspeito = self.suspeito_service.get_by_id(suspeito_id)
        
        if suspeito is None:
            raise ValueError(f'id de suspeito {suspeito_id} não existe!')

        for numero_suspeito in suspeito.numerosuspeito:
            numero = numero_suspeito.numero
            if not self.numero_service.numeroIsOnOperation(suspeito_id, operation_ids):
                continue

            telefone = numero.numero
            identificacao = telefone
            
            if suspeito.nome:
                identificacao = suspeito.nome
            elif suspeito.apelido:
                identificacao = suspeito.apelido
            
            nodes.append({"id": identificacao, "group": self.SUSPEITO})

            relations = self.mensagem_service.count_mensagens_por_alvo(numero)
            for target, value in relations.items():
                links.append({"source": identificacao, "target": target, "value": value})