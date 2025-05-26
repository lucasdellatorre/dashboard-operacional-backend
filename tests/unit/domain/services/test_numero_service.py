from unittest.mock import Mock
from app.domain.services.numeroservice import NumeroService
from app.domain.entities.numero import Numero


def test_find_returns_numero():
    # Arrange
    mock_repo = Mock()
    numero_id = 123
    expected_numero = Numero(id=numero_id, numero="5555")
    mock_repo.find.return_value = expected_numero
    service = NumeroService(mock_repo)

    # Act
    result = service.find(numero_id)

    # Assert
    mock_repo.find.assert_called_once_with(numero_id)
    assert result == expected_numero


def test_isAlvo_returns_true():
    # Arrange
    mock_repo = Mock()
    numero_id = 123
    mock_repo.isAlvo.return_value = True
    service = NumeroService(mock_repo)

    # Act
    result = service.isAlvo(numero_id)

    # Assert
    mock_repo.isAlvo.assert_called_once_with(numero_id)
    assert result is True
