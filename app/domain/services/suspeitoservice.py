from app.domain.repositories.suspeitorepository import ISuspeitoRepository
from app.domain.entities.suspeito import Suspeito as SuspeitoEntity

class SuspeitoService:
    def __init__(self, suspeito_repository: ISuspeitoRepository):
        self.suspeito_repository = suspeito_repository

    def get_by_id(self, id: int) -> SuspeitoEntity | None:
        return self.suspeito_repository.get_by_id_with_relations(id)

    def get_suspeito_by_numero_id(self, numero_id: int) -> dict | None:
        suspeito = self.suspeito_repository.get_by_numero_id_with_relations(numero_id)

        if not suspeito:
            return None

        return {
            "apelido": suspeito.apelido,
            "numeros": [num.numero for num in suspeito.numeros]
        }
