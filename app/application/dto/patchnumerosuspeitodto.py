from dataclasses import dataclass

@dataclass
class PatchNumeroSuspeitoDTO():
    numerosIds: list[int]
    suspeitoId: int
    cpf: str
    
    