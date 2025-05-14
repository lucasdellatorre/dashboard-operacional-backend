from app.domain.repositories.usuariorepository import IUsuarioRepository
from app.domain.entities.usuario import Usuario

class UsuarioService:
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    def create_usuario(self, cpf: str) -> Usuario:
        usuario = Usuario(cpf=cpf)
        return self.usuario_repository.create(usuario)