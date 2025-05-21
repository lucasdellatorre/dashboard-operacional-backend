from typing import List
from app.domain.entities.mensagem import Mensagem
from app.domain.repositories.mensagemiprepository import IMensagemIPRepository

class IpmensagemService:
    def __init__(self, filtro_mensagem_repository: IMensagemIPRepository):
        self.filtro_mensagem_repository = filtro_mensagem_repository

    def buscar_mensagens_por_ip(self, filtro: Mensagem) -> List[Mensagem]:
        return self.filtro_mensagem_repository.buscar_mensagens_por_ip(filtro)
