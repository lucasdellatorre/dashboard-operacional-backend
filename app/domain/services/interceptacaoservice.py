from app.domain.repositories.interceptacaorepository import IInterceptacaoRepository
from app.domain.entities.interceptacao import Interceptacao as InterceptacaoEntity

class InterceptacaoService:
    def __init__(self, interceptacao_repository: IInterceptacaoRepository):
        self.interceptacao_repository = interceptacao_repository

    def get_interceptacoes_por_operacoes(self, operacao_ids: list[int]) -> list[InterceptacaoEntity]:
        """
        Retorna todas as interceptações associadas às operações fornecidas.
        """
        return self.interceptacao_repository.get_by_operacao_ids(operacao_ids)
