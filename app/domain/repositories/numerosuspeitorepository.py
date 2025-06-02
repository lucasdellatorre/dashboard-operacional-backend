from abc import ABC, abstractmethod

class INumeroSuspeitoRepository(ABC):
    @abstractmethod
    def count_by_suspeito(self, suspeito_id: int) -> int:
        raise (NotImplementedError)

    @abstractmethod
    def delete_relacao(self, suspeito_id: int, numero_id: int) -> bool:
        raise (NotImplementedError)