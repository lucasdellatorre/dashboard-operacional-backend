from app.application.dto.usuariodto import UsuarioDTO
from app.domain.services.usuarioservice import UsuarioService

class CreateUserUseCase:
    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service

    def execute(self, usuario_dto: UsuarioDTO) -> UsuarioDTO:
        cpf = usuario_dto.cpf
        new_user = self.usuario_service.create_usuario(cpf)
        return UsuarioDTO.fromEntity(new_user)