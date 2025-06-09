from app.application.dto.patchnumerosuspeitodto import PatchNumeroSuspeitoDTO
from app.domain.services.numeroservice import NumeroService
from app.domain.services.suspeitoservice import SuspeitoService

class AdicionaNumeroSuspeitoUseCase:
    def __init__(self, numero_service: NumeroService, suspeito_service: SuspeitoService):
        self.numero_service = numero_service
        self.suspeito_service = suspeito_service

    def execute(self, request: PatchNumeroSuspeitoDTO) -> bool:
        numeros_ids = request.numerosIds
        res = []
        
        for numeroId in numeros_ids:
            if not(self.numero_service.isNumero(numeroId)):
                return False
        
            if not self.suspeito_service.is_suspeito(request.suspeitoId): 
                return False
            
            res.append(self.suspeito_service.add_telefone(request.suspeitoId, numeroId, request.cpf))
        
        return all(res)
