from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.mensagem import Mensagem as DomainMensagem

class IMensagemRepository(ABC):
    @abstractmethod
    def get_mensagens_from_numero_id(self, numero_id) -> list[DomainMensagem]:
        raise (NotImplementedError)
    
    @abstractmethod
    def contar_mensagens_por_contato(
        self,
        numeros: List[str],
        tickets: List[str],
        tipo: str,
        grupo: str,
        data_inicial: str,
        data_final: str,
        hora_inicio: str,
        hora_fim: str
    ) -> List[dict]:
        """
        Retorna uma lista com a contagem de mensagens por contato, com base nos filtros fornecidos.
        Cada item do resultado é um dicionário com:
        {
            "contato": str,
            "qtdMensagens": int
        }
        """
        raise NotImplementedError