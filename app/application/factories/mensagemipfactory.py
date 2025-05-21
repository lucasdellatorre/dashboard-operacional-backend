from app.adapters.repositories.mensagemiprepository import MensagemIPRepository
from app.domain.services.ipmensagemservice import IpmensagemService
from app.application.usecases.buscarmensagemporipusecase import BuscarMensagemPorIPUseCase

class MensagemIpFactory:
    @staticmethod
    def buscar_mensagens_por_ip() -> BuscarMensagemPorIPUseCase:
        repository = MensagemIPRepository()
        service = IpmensagemService(repository)
        return BuscarMensagemPorIPUseCase(service)
