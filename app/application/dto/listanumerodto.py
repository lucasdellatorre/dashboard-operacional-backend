from datetime import date, datetime

class ListaNumeroDTO:
    def __init__(self, numeroId, numero, relevante, isAlvo, dataUpload, operacoes, apelido=None, suspeitoId=None):
        self.numeroId = numeroId
        self.numero = numero
        self.relevante = relevante
        self.isAlvo = isAlvo
        self.dataUpload = dataUpload
        self.operacoes = operacoes
        self.apelido = apelido
        self.suspeitoId = suspeitoId

    def to_dict(self) -> dict:
        return {
            "id": self.numeroId,
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
    def from_dict(row: dict) -> 'ListaNumeroDTO':
        return ListaNumeroDTO(
            numeroId=row["numeroId"],  # <– mudou aqui
            numero=row["numero"],
            relevante=row["relevante"],
            isAlvo=bool(row["isAlvo"]),
            dataUpload=row["dataUpload"],
            operacoes=row.get("operacoes", []),
            apelido=row.get("apelido"),
            suspeitoId=row.get("suspeitoId")
        )
    
    @staticmethod
    def group_by_suspeito(lista_dtos: list['ListaNumeroDTO']) -> dict:
        suspeitos_dict = {}
        numeros_list = []

        for dto in lista_dtos:
            if dto.apelido and dto.suspeitoId:
                if dto.suspeitoId not in suspeitos_dict:
                    suspeitos_dict[dto.suspeitoId] = {
                        "id": dto.suspeitoId,
                        "apelido": dto.apelido,
                        "relevante": dto.relevante,
                        "operacoes": {op["id"] for op in dto.operacoes},
                        "numeros": {dto.numero},
                        "data_criacao": dto.dataUpload.isoformat()
                            if isinstance(dto.dataUpload, (date, datetime))
                            else dto.dataUpload
                    }
                else:
                    suspeitos_dict[dto.suspeitoId]["operacoes"].update(op["id"] for op in dto.operacoes)
                    suspeitos_dict[dto.suspeitoId]["numeros"].add(dto.numero)
            else:
                numeros_list.append(dto.to_dict())

        suspeitos = []
        for s in suspeitos_dict.values():
            s["operacoes"] = list(s["operacoes"])
            s["numeros"] = list(s["numeros"])
            suspeitos.append(s)

        return {
            "suspeitos": suspeitos,
            "numeros": numeros_list
        }