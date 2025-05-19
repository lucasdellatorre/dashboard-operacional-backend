from app.domain.services.numeroservice import NumeroService
from app.application.dto.listanumerodto import ListaNumeroDTO

class GetOperationTargetsUseCase:
    def __init__(self, numero_service: NumeroService):
        self.numero_service = numero_service

    def execute(self, operacao_ids: list[int]):
        rows = self.numero_service.listarNumeroOperacao(operacao_ids)
        return [ListaNumeroDTO.from_dict(row) for row in rows]
