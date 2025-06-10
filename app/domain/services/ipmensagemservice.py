from typing import List
from app.domain.entities.mensagem import Mensagem
from app.application.dto.filtromensagemdto import FiltroMensagemDTO
from app.domain.repositories.mensagemiprepository import IMensagemIPRepository
from app.application.dto.mensagemporipresponsedto import MensagemPorIpResponseDTO


class IpmensagemService:
    def __init__(self, filtro_mensagem_repository: IMensagemIPRepository):
        self.filtro_mensagem_repository = filtro_mensagem_repository

    def buscar_mensagens_por_ip(self, filtro: FiltroMensagemDTO, tickets: list[str]) -> List[MensagemPorIpResponseDTO]:
        return self.filtro_mensagem_repository.buscar_mensagens_por_ip(filtro, tickets)
