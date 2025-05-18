from abc import ABC, abstractmethod

class ISuspeitoRepositoryInterface(ABC):
    @abstractmethod
    def atualizar(self, id: int, dados: dict) -> dict:
        raise (NotImplementedError)


