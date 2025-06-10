from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.interceptacao import Interceptacao

class IInterceptacaoRepository(ABC):
    @abstractmethod
    def get_by_operacao_ids(self, operacao_ids: List[int]) -> List[Interceptacao]:
        pass