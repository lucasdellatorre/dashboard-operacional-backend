from app.application.dto.suspeitoupdatedto import SuspeitoUpdateDTO
from app.domain.services.suspeitoservice import SuspeitoService

class SuspeitoUseCase:
    def __init__(self, service: SuspeitoService):
        self.service = service

    def atualizar_suspeito(self, id, data):
        dto = SuspeitoUpdateDTO(**data)
        return self.service.atualizar_suspeito(id, dto.to_dict())
