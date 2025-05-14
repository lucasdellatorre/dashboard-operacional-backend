from abc import ABC, abstractmethod

class TestRepository(ABC):
    @abstractmethod
    def say_hi(self) -> str:
        raise (NotImplementedError)