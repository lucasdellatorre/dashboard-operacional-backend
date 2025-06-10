from abc import ABC, abstractmethod
from typing import List, Optional
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
    def buscar_por_filtro(
            self,
            numeros: List[str],
            tickets: List[str],
            tipo: Optional[str],
            grupo: Optional[str],
            data_inicial: Optional[str],
            data_final: Optional[str],
            hora_inicio: Optional[str],
            hora_fim: Optional[str],
            dias_semana: Optional[List[int]]
    ) -> List[dict]:
        raise NotImplementedError