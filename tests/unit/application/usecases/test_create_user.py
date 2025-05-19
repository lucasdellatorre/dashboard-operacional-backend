from unittest.mock import Mock
from app.application.usecases.createuserusecase import CreateUserUseCase
from app.application.dto.usuariodto import UsuarioDTO
from app.domain.entities.usuario import Usuario


def test_execute_creates_user_successfully():
    # Arrange
    mock_service = Mock()
    input_dto = UsuarioDTO(cpf="12345678900")

    created_user = Usuario(id=1, cpf="12345678900")
    mock_service.create_usuario.return_value = created_user

    use_case = CreateUserUseCase(mock_service)

    # Act
    result = use_case.execute(input_dto)

    # Assert
    mock_service.create_usuario.assert_called_once_with("12345678900")
    assert isinstance(result, UsuarioDTO)
    assert result.cpf == "12345678900"