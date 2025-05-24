from app.adapters.repositories.numerorepository import NumeroRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.application.usecases.teiamessagecount import TeiaMessageCountUseCase
from app.domain.services.numeroservice import NumeroService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.suspeitoservice import SuspeitoService

class TeiaFactory:
    @staticmethod
    def message_count():
        msg_repository = MensagemRepository()
        numero_repository = NumeroRepository()
        suspeito_repository = SuspeitoRepository()
        numero_service = NumeroService(numero_repository)
        msg_service = MensagemService(msg_repository)
        suspeito_service = SuspeitoService(suspeito_repository, numero_repository)
        return TeiaMessageCountUseCase(numero_service, msg_service, suspeito_service)