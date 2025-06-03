from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MensagensDiaSemanaRequestDTO:
    dias_semana: list[str]

@dataclass
class MensagensDiaSemanaResponseDTO:
    dias: List[Dict[str, int]]

    def to_dict(self):
        return{
            "dias": self.dias
        }
