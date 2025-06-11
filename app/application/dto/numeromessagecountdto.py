from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class NumeroMessageCountRequestDTO:
    numeros: List[int]  # Tipa explicitamente como lista de IDs de números

@dataclass
class NumeroMessageCountResponseDTO:
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    links: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": self.nodes,
            "links": self.links
        }
