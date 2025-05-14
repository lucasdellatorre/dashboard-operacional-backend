from abc import ABC, abstractmethod
from app.domain.entities.usuario import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    def create(self, user: Usuario) -> Usuario:
        raise (NotImplementedError)