from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.mensagem import Mensagem as DomainMensagem
from typing import List, Dict

class IMensagemRepository(ABC):
    @abstractmethod
    def get_mensagens_from_numero_id(self, numero_id) -> list[DomainMensagem]:
        raise (NotImplementedError)

    @abstractmethod
    def get_mensagens_by_ip(self, ip_id: int) -> List[DomainMensagem]:
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

    @abstractmethod
    def contar_mensagens_por_horario(
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
        Retorna uma lista com a contagem de mensagens agrupadas por faixa de horário de 2 horas.
        Cada item do resultado é um dicionário com:
        {
            "periodo": str,         # Ex: "00:00-02:00", "02:00-04:00", etc.
            "qtdMensagens": int
        }
        """
        raise NotImplementedError
    
    @abstractmethod
    def contar_mensagens_por_dia(
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
        Retorna uma lista com a contagem de mensagens por dia, com base nos filtros fornecidos.
        Cada item do resultado é um dicionário com:
        {
            "data": str,            # Ex: "2023-10-01"
            "qtdMensagens": int
        }
        """
        raise NotImplementedError