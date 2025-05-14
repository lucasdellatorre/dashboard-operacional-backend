from app.adapters.repositories.userrepository import UserRepository
from app.application.usecases.createuserusecase import CreateUserUseCase
from app.domain.services.usuarioservice import UsuarioService

class UserFactory:
    @staticmethod
    def create_user():
        user_repository = UserRepository()
        user_service = UsuarioService(user_repository)
        return CreateUserUseCase(user_service)