from typing import List
from app.domain.entities.mensagem import Mensagem
from app.application.dto.filtromensagemdto import FiltroMensagemDTO
from app.domain.repositories.mensagemdiarepository import IMensagemDiaRepository

class DiamensagemService:
    def __init__(self, filtro_mensagem_repository: IMensagemDiaRepository):
        self.filtro_mensagem_repository = filtro_mensagem_repository

    def buscar_mensagens_por_dia(self, filtro: FiltroMensagemDTO) -> List[Mensagem]:
        # lista de dias com a quantidade de mensagens -- dias com mensagens > 0 
        # chamar funcao get day of week

        # retorna o dto correto
        return self.filtro_mensagem_repository.buscar_mensagens_por_ip(filtro)

    
    # funcao para descobrir dia da semana - recebe lista de dias
        # agrupar os dias por dias da semana e somar a quant de msgs
            # retorna os valores