from app.domain.repositories.numerosuspeitorepository import INumeroSuspeitoRepository

class NumeroSuspeitoService:
    def __init__(self, repository: INumeroSuspeitoRepository):
        self.repository = repository

    def remover_relacionamento(self, suspeito_id: int, numero_id: int) -> bool:
        count = self.repository.count_by_suspeito(suspeito_id)
        if count <= 1:
            return False
        return self.repository.delete_relacao(suspeito_id, numero_id)
