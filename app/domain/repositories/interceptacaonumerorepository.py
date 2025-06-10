from abc import ABC, abstractmethod

class IInterceptacaoNumeroRepository(ABC):
    @abstractmethod
    def listar_numeros_com_suspeito(self) -> list[dict]:
        """
        Retorna uma lista de números interceptados com dados do suspeito,
        se houver (apelido e números vinculados).
        """
        pass

    @abstractmethod
    def get_all_alvos(self) -> list[dict]:
        """
        Retorna todos os números interceptados
        """
        pass

    @abstractmethod
    def get_alvos_by_interceptacoes(self, tickets: list[str]) -> list[str]:
        pass