from app.domain.repositories.suspeitorepository import ISuspeitoRepository
from app.domain.entities.suspeito import Suspeito as SuspeitoEntity

class SuspeitoService:
    def __init__(self, suspeito_repository: ISuspeitoRepository):
        self.suspeito_repository = suspeito_repository

    def get_by_id(self, id: int) -> SuspeitoEntity | None:
        suspeito = self.suspeito_repository.get_by_id_with_relations(id)
        
        if not suspeito:
            return None
    
        return suspeito
