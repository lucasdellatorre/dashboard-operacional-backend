from datetime import datetime
from typing import List, Optional
from app.domain.entities.mensagem import Mensagem

class FiltroMensagemDTO:
    def __init__(
        self,
        numero: List[str],
        operacoes: List[str] = None,
        grupo: Optional[str] = None,
        tipo: Optional[str] = None,
        data_inicial: Optional[str] = None,
        data_final: Optional[str] = None,
        hora_inicial: Optional[str] = None,
        hora_final: Optional[str] = None,
        dias_semana: Optional[List[int]] = None,
    ):
        self.numero = numero
        self.operacoes = operacoes
        self.grupo = grupo
        self.tipo = tipo
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.dias_semana = dias_semana

    def to_dict(self):
        return {
            "numero": self.numero,
            "operacoes": self.operacoes,
            "grupo": self.grupo,
            "tipo": self.tipo,
            "data_inicial": self.data_inicial,
            "data_final": self.data_final,
            "hora_inicial": self.hora_inicial,
            "hora_final": self.hora_final,
            "dias_semana": self.dias_semana,
        }