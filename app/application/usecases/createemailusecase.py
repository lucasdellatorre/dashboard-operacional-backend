from app.application.dto.createemaildto import CreateEmailDTO
from app.domain.entities.suspeitoemail import SuspeitoEmail
from app.domain.services.suspeitoservice import SuspeitoService

class CreateEmailUseCase:
    def __init__(self, suspeito_service: SuspeitoService):
        self.suspeito_service = suspeito_service

    def execute(self, dto: CreateEmailDTO) -> bool:
        suspeito_entity = self.suspeito_service.get_by_id(dto.suspeitoId)

        if not suspeito_entity:
            raise ValueError(f"Não existe um suspeito com o id {dto.suspeitoId}")

        # Verifica se o e-mail já existe, comparando diretamente o valor
        for email_obj in suspeito_entity.emails:
            if email_obj.email.strip().lower() == dto.email.strip().lower():
                raise ValueError(f"O e-mail '{dto.email}' já está associado ao suspeito {dto.suspeitoId}")

        email = SuspeitoEmail(
            suspeitoId=dto.suspeitoId,
            lastUpdateCpf=dto.cpf,
            email=dto.email
        )

        return self.suspeito_service.create_email(email)