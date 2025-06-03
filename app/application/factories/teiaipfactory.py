from app.adapters.repositories.iprepository import IPRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository
from app.application.usecases.teiaipmessagecountusecase import TeiaIPMessageCountUseCase
from app.domain.services.teiaipservice import TeiaIPService
from app.domain.services.mensagemservice import MensagemService

class TeiaIPFactory:
    @staticmethod
    def message_count():
        ip_repository = IPRepository()
        mensagem_repository = MensagemRepository()
        teia_ip_service = TeiaIPService(ip_repository)
        mensagem_service = MensagemService(mensagem_repository)
        return TeiaIPMessageCountUseCase(teia_ip_service, mensagem_service)