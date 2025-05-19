import pytest
from unittest.mock import Mock
from app.application.usecases.createsuspeitousecase import CreateSuspeitoUseCase
from app.application.dto.createsuspeitodto import CreateSuspeitoDTO
from app.application.dto.suspeitodto import SuspeitoDTO
from app.domain.entities.suspeito import Suspeito


def test_execute_creates_suspeito_successfully():
    # Arrange
    mock_service = Mock()
    dto = CreateSuspeitoDTO(apelido="João", numeros_ids=[1, 2])

    mock_service.find_by_name.return_value = None

    created_entity = Suspeito(id=1, apelido="João", numerosuspeito=[])
    mock_service.create_suspeito.return_value = created_entity

    use_case = CreateSuspeitoUseCase(mock_service)

    # Act
    result = use_case.execute(dto)

    # Assert
    mock_service.find_by_name.assert_called_once_with("João")
    mock_service.create_suspeito.assert_called_once_with(dto)
    assert isinstance(result, SuspeitoDTO)
    assert result.apelido == "João"


def test_execute_raises_if_apelido_missing():
    # Arrange
    mock_service = Mock()
    dto = CreateSuspeitoDTO(apelido="", numeros_ids=[1])

    use_case = CreateSuspeitoUseCase(mock_service)

    # Act & Assert
    with pytest.raises(ValueError, match="Apelido é obrigatório."):
        use_case.execute(dto)

    mock_service.find_by_name.assert_not_called()
    mock_service.create_suspeito.assert_not_called()


def test_execute_raises_if_numeros_ids_empty():
    # Arrange
    mock_service = Mock()
    dto = CreateSuspeitoDTO(apelido="Carlos", numeros_ids=[])

    use_case = CreateSuspeitoUseCase(mock_service)

    # Act & Assert
    with pytest.raises(ValueError, match="Pelo menos um número deve ser fornecido."):
        use_case.execute(dto)

    mock_service.find_by_name.assert_not_called()
    mock_service.create_suspeito.assert_not_called()


def test_execute_raises_if_apelido_already_exists():
    # Arrange
    mock_service = Mock()
    dto = CreateSuspeitoDTO(apelido="João", numeros_ids=[1])

    mock_service.find_by_name.return_value = Suspeito(id=99, apelido="João", numerosuspeito=[])

    use_case = CreateSuspeitoUseCase(mock_service)

    # Act & Assert
    with pytest.raises(ValueError, match="Apelido já cadastrado."):
        use_case.execute(dto)

    mock_service.find_by_name.assert_called_once_with("João")
    mock_service.create_suspeito.assert_not_called()
