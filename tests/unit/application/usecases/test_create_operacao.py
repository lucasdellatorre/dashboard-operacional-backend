import pytest
from unittest.mock import Mock
from app.application.usecases.createoperacaousecase import CreateOperacaoUseCase
from app.application.dto.operacaodto import OperacaoDTO
from app.domain.entities.operacao import Operacao


def test_execute_creates_new_operation_when_name_not_exists():
    # Arrange
    mock_service = Mock()
    operacao_dto = OperacaoDTO(nome="Operação X")
    mock_service.find_by_name.return_value = None

    created_operacao = Operacao(id=1, nome="Operação X", dataCriacao="2025-01-01")
    mock_service.create_operacao.return_value = created_operacao

    use_case = CreateOperacaoUseCase(mock_service)

    # Act
    result = use_case.execute(operacao_dto)

    # Assert
    mock_service.find_by_name.assert_called_once_with("Operação X")
    mock_service.create_operacao.assert_called_once_with("Operação X")
    assert isinstance(result, OperacaoDTO)
    assert result.nome == "Operação X"


def test_execute_raises_value_error_when_operation_exists():
    # Arrange
    mock_service = Mock()
    operacao_dto = OperacaoDTO(nome="Operação Existente")
    mock_service.find_by_name.return_value = Mock()  # simulate existing operation

    use_case = CreateOperacaoUseCase(mock_service)

    # Act & Assert
    with pytest.raises(ValueError, match="operation already exists!"):
        use_case.execute(operacao_dto)

    mock_service.find_by_name.assert_called_once_with("Operação Existente")
    mock_service.create_operacao.assert_not_called()
