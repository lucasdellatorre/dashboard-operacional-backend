from app.domain.services.suspeitoservice import SuspeitoService


class UpdateEmailUseCase:
    def __init__(self, suspeito_service: SuspeitoService):
        self.suspeito_service = suspeito_service

    def execute(self, dto):
        return self.suspeito_service.update_email(dto)