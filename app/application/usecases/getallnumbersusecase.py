from app.domain.services.numeroservice import NumeroService
from app.application.dto.numerosimplesdto import NumeroSimplesDTO

class GetAllNumbersUseCase:
    def __init__(self, numero_service: NumeroService):
        self.numero_service = numero_service

    def execute(self) -> list[dict]:
        return self.numero_service.listar_numeros()