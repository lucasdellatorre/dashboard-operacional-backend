from app.domain.services.suspeitoservice import SuspeitoService

class DeleteEmailUseCase:
    def __init__(self, suspeito_service: SuspeitoService):
        self.suspeito_service = suspeito_service

    def execute(self, suspeitoId, emailId) -> bool:
        suspeito_entity = self.suspeito_service.get_by_id(suspeitoId)

        if not suspeito_entity:
            raise ValueError(f'Não existe um suspeito com o id {suspeitoId}')

        return self.suspeito_service.delete_email(suspeitoId, emailId)
