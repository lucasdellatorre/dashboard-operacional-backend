from unittest.mock import Mock
from app.domain.entities.usuario import Usuario
from app.domain.services.usuarioservice import UsuarioService

def test_create_usuario_returns_created_usuario():
    # Arrange
    mock_repository = Mock()
    cpf = "12345678900"
    expected_usuario = Usuario(cpf=cpf)
    
    # Mocking repository.create to return expected_usuario
    mock_repository.create.return_value = expected_usuario
    
    service = UsuarioService(usuario_repository=mock_repository)

    # Act
    result = service.create_usuario(cpf)

    # Assert
    mock_repository.create.assert_called_once()
    assert result == expected_usuario
    assert result.cpf == cpf