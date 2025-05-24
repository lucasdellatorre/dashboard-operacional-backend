from app.application.dto.suspeitodetalhadodto import SuspeitoDetalhadoDTO
from app.domain.services.suspeitoservice import SuspeitoService

class GetSuspeitoByIdUseCase:
    def __init__(self, suspeito_service: SuspeitoService):
        self.suspeito_service = suspeito_service

    def execute(self, id: int) -> SuspeitoDetalhadoDTO | None:
        suspeito_entity = self.suspeito_service.get_by_id(id)

        if not suspeito_entity:
            return None

        return SuspeitoDetalhadoDTO.from_entity(suspeito_entity)
