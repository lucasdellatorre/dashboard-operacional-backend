from datetime import datetime
from typing import List, Optional
from app.domain.entities.mensagem import Mensagem


class MensagemResponseDTO:
    def __init__(self, numero: str, ip:str, total: int):
        self.numero = numero
        self.ip = ip
        self.total = total

    def to_dict(self) -> dict:  
        return {
            "numero": self.numero,
            "ip": self.ip,
            "total":  self.total
        }

    @classmethod
    def from_ocorrencias(cls, numero: str, ocorrencias: List[Mensagem]) -> "MensagemResponseDTO":
        total = len(ocorrencias)
        ip = next(
          (m.remetenteIp for m in ocorrencias if m.remetente == numero),
          None
        )
        return cls(numero=numero, ip=ip, total=total)
    
