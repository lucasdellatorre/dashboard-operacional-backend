from app.domain.entities.numero import Numero
from typing import Optional

class NumeroSuspeito:
    def __init__(
        self,
        numero: Numero,
        lastUpdateCpf: Optional[str] = None,
        lastUpdateDate: Optional[str] = None
    ):
        self.numero = numero
        self.lastUpdateCpf = lastUpdateCpf
        self.lastUpdateDate = lastUpdateDate
