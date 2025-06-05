from app.domain.services.numerosuspeitoservice import NumeroSuspeitoService

class DeleteNumeroSuspeitoUseCase:
    def __init__(self, service: NumeroSuspeitoService):
        self.service = service

    def execute(self, suspeito_id: int, numero_id: int) -> bool:
        return self.service.remover_relacionamento(suspeito_id, numero_id)
