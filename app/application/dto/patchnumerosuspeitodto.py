from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PatchNumeroSuspeitoDTO():
    numero_id: list[int]
    suspeito_id: int
    cpf: str
    lastUpdateDate: datetime = field(default_factory = datetime.now(), init = False)
    