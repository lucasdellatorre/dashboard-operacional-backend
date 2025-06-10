from app.application.dto.suspeitoupdatedto import SuspeitoUpdateDTO
from app.domain.services.suspeitoservice import SuspeitoService

class AtualizarSuspeitoUseCase:
    def __init__(self, service: SuspeitoService):
        self.service = service

    def atualizar_suspeito(self, id, dto: SuspeitoUpdateDTO):
        entidade = self.service.atualizar_suspeito(id, dto.to_dict())
        return SuspeitoUpdateDTO.fromEntity(entidade)