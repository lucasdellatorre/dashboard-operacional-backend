from app.adapters.repositories.numerorepository import NumeroRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository
from app.application.usecases.teiamessagecount import TeiaMessageCountUseCase
from app.domain.services.numeroservice import NumeroService
from app.domain.services.mensagemservice import MensagemService

class TeiaFactory:
    @staticmethod
    def message_count():
        msg_repository = MensagemRepository()
        numero_repository = NumeroRepository()
        numero_service = NumeroService(numero_repository)
        msg_service = MensagemService(msg_repository)
        return TeiaMessageCountUseCase(numero_service, msg_service)