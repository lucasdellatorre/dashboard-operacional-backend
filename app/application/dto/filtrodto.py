from typing import List, Optional

class FiltroDTO:
    def __init__(
            self,
            numero: Optional[List[str]] = None,
            operacoes: Optional[List[str]] = None,
            grupo: Optional[str] = None,
            tipo: Optional[str] = None,
            data_inicial: Optional[str] = None,
            data_final: Optional[str] = None,
            hora_inicial: Optional[str] = None,
            hora_final: Optional[str] = None,
            dias_semana: Optional[List[int]] = None,
    ):
        self.numero = numero or []
        self.operacoes = operacoes or []
        self.grupo = grupo
        self.tipo = tipo
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.dias_semana = dias_semana or []
