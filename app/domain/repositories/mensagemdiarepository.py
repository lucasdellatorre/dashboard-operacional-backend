from abc import ABC, abstractmethod
from typing import List
from app.application.dto.filtromensagemdto import FiltroMensagemDTO
from app.domain.entities.mensagem import Mensagem

class IMensagemDiaRepository(ABC):
    @abstractmethod
    def buscar_mensagens_por_dia(self, filtro: FiltroMensagemDTO) -> List[Mensagem]:
        pass

    @abstractmethod
    def count_mensagens_por_dia(self)
        pass

    @abstractmethod
    def get_dia_semana_por_data(self)
        pass
    
