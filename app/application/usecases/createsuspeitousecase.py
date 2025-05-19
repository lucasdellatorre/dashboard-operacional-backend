from app.application.dto.createsuspeitodto import CreateSuspeitoDTO
from app.application.dto.suspeitodto import SuspeitoDTO
from app.domain.services.suspeitoservice import SuspeitoService

class CreateSuspeitoUseCase:
    def __init__(self, suspeito_service: SuspeitoService):
        self.suspeito_service = suspeito_service

    def execute(self, dto: CreateSuspeitoDTO):
        if not dto.apelido:
            raise ValueError("Apelido é obrigatório.")
        if not dto.numeros_ids or len(dto.numeros_ids) == 0:
            raise ValueError("Pelo menos um número deve ser fornecido.")
        if self.suspeito_service.find_by_name(dto.apelido):
            raise ValueError("Apelido já cadastrado.")

        entity = self.suspeito_service.create_suspeito(dto)
        return SuspeitoDTO.fromEntity(entity)
