from app.application.dto.createemaildto import CreateEmailDTO
from app.domain.entities.suspeitoemail import SuspeitoEmail
from app.domain.services.suspeitoservice import SuspeitoService

class GetAllEmailUseCase:
    def __init__(self, suspeito_service: SuspeitoService):
        self.suspeito_service = suspeito_service

    def execute(self, id) -> list[SuspeitoEmail]:
        suspeito_entity = self.suspeito_service.get_by_id(id)

        if not suspeito_entity:
            raise ValueError(f'Não existe um suspeito com o id {id}')

        return self.suspeito_service.get_all_email(id)
