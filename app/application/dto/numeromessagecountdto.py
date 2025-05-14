from dataclasses import dataclass

@dataclass
class NumeroMessageCountRequestDTO():
    numeros: list
    
@dataclass
class NumeroMessageCountResponseDTO():
    nodes: list
    links: list
    
    def to_dict(self):
        return {
            "nodes": self.nodes,
            "links": self.links
        }
    