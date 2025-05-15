from datetime import date, datetime
class ListaOperacaoDTO:
    def __init__(self, id, numero, relevante, isAlvo, dataUpload, operacoes):
        self.id = id
        self.numero = numero
        self.relevante = relevante
        self.isAlvo = isAlvo
        self.dataUpload = dataUpload
        self.operacoes = operacoes

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero": self.numero,
            "relevante": self.relevante,
            "isAlvo": self.isAlvo,
            "dataUpload": (
                self.dataUpload.isoformat()
                if isinstance(self.dataUpload, (date, datetime))
                else self.dataUpload
            ),
            "operacoes": self.operacoes
        }

    @staticmethod
    def from_dict(row: dict) -> 'ListaOperacaoDTO':
        return ListaOperacaoDTO(
            id=row["id"],
            numero=row["numero"],
            relevante=row["relevante"],
            isAlvo=bool(row["isAlvo"]),
            dataUpload=row["dataUpload"],
            operacoes=row.get("operacoes", [])  
        )