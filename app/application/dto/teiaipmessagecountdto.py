from dataclasses import dataclass

@dataclass
class TeiaIPMessageCountRequestDTO:
    ip_ids: list

@dataclass
class TeiaIPMessageCountResponseDTO:
    nodes: list
    links: list

    def to_dict(self):
        return {
            "nodes": self.nodes,
            "links": self.links
        }