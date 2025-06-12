from dataclasses import dataclass, field
from typing import Any, Dict, List

class TeiaIPMessageCountRequestDTO:
    def __init__(self, numeros, suspeitos, operacoes, data_inicial, data_final, hora_inicio, hora_fim):
        self.numeros = numeros or []
        self.suspeitos = suspeitos or []
        self.operacoes = operacoes
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
    
    @classmethod
    def from_dict(cls, data: dict):
        # Validação básica obrigatória
        operacoes = data.get("operacoes")
        if operacoes and not isinstance(operacoes, list):
            raise ValueError("A lista de operações é obrigatória e deve ser uma lista.")

        return cls(
            numeros=data.get("numeros", []),
            suspeitos=data.get("suspeitos", []),
            operacoes=operacoes,
            data_inicial=data.get("data_inicial"),
            data_final=data.get("data_final"),
            hora_inicio=data.get("hora_inicio"),
            hora_fim=data.get("hora_fim")
        )

@dataclass
class NumeroMessageCountResponseDTO:
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    links: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": self.nodes,
            "links": self.links
        }
