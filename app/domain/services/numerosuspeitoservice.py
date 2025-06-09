from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.repositories.suspeitorepository import ISuspeitoRepository

class NumeroSuspeitoService():
    def __init__(self, numero_repository = INumeroRepository, suspeito_repository = ISuspeitoRepository):
        self.suspeito_repository = suspeito_repository
        self.numero_repository = numero_repository 

    def listar_numeros_suspeito(self, suspeito_id):
        return self.repository.listar_numeros_suspeito(suspeito_id)
        
    def adicionar_numeros_suspeito(self, cpf, suspeito_id, numero_id):
        return self.repository.adicionar_numeros_suspeito(cpf, suspeito_id, numero_id)

    def remover_relacionamento(self, suspeito_id: int, numero_id: int) -> bool:
        count = self.repository.count_by_suspeito(suspeito_id)
        if count <= 1:
            return False
        return self.repository.delete_relacao(suspeito_id, numero_id)
