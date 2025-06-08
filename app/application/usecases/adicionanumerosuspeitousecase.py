from app.application.dto.patchnumerosuspeitodto import PatchNumeroSuspeitoDTO
from app.domain.services.numeroservice import NumeroService
from app.domain.services.suspeitoservice import SuspeitoService

class AdicionaNumeroSuspeitoUseCase:
    def __init__(self, numero_service: NumeroService, suspeito_service: SuspeitoService):
        self.numero_service = numero_service
        self.suspeito_service = suspeito_service

    def execute(self, request: PatchNumeroSuspeitoDTO):
        numeros_ids = request.numero_id
        
        for numero_id in numeros_ids:
            if not(self.numero_service.isNumero(numero_id)):
                return False
        
        if not self.suspeito_service.is_suspeito(request.suspeito_id): 
            return False
