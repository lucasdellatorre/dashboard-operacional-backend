from app.adapters.repositories.mensagemdiarepository import MensagemDiaRepository
from app.domain.services.diamensagemservice import DiamensagemService
from app.application.usecases.buscarmensagempordiausecase import BuscarMensagemPorDiaUseCase

class MensagemDiaFactory:
    @staticmethod
    def buscar_mensagens_por_dia() -> BuscarMensagemPorDiaUseCase:
        repository = MensagemDiaRepository()
        service = DiamensagemService(repository)
        return BuscarMensagemPorDiaUseCase(service)
