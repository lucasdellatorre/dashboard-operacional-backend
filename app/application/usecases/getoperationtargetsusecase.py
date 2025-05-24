from app.domain.services.numeroservice import NumeroService

class GetOperationTargetsUseCase:
    def __init__(self, numero_service: NumeroService):
        self.numero_service = numero_service

    def execute(self, operacao_ids: list[int]) -> dict:
        return self.numero_service.listarNumeroOperacao(operacao_ids)