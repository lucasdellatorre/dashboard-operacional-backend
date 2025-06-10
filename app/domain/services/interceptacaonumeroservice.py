from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero
from app.adapters.repositories.entities.numero import Numero
from app.adapters.repositories.entities.numerosuspeito import NumeroSuspeito
from app.adapters.repositories.entities.suspeito import Suspeito
from app.domain.repositories.interceptacaonumerorepository import IInterceptacaoNumeroRepository

class InterceptacaoNumeroService:
    def __init__(self, repository: IInterceptacaoNumeroRepository):
        self.repository = repository

    def listar_numeros_com_suspeito_e_numeros(self) -> list[dict]:
        return self.repository.listar_numeros_com_suspeito()
    
    def get_all_numeros(self) -> list[dict]:
        return self.repository.get_all_alvos()
    
    def get_alvos_por_interceptacoes(self, tickets: list[str]) -> list[dict]:
        if not tickets:
            return []
        
        return self.repository.get_alvos_by_interceptacoes(tickets)