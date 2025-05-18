from unittest.mock import Mock
from app.domain.services.operacaoservice import OperacaoService
from app.domain.entities.operacao import Operacao


def test_has_operacao_returns_true():
    # Arrange
    mock_repo = Mock()
    mock_repo.hasOperacao.return_value = True
    service = OperacaoService(mock_repo)

    # Act
    result = service.hasOperacao(1)

    # Assert
    mock_repo.hasOperacao.assert_called_once_with(1)
    assert result is True


def test_get_all_operacoes_returns_list():
    # Arrange
    mock_repo = Mock()
    expected_result = ["op1", "op2"]
    mock_repo.get_all_operations.return_value = expected_result
    service = OperacaoService(mock_repo)

    # Act
    result = service.get_all_operacoes()

    # Assert
    mock_repo.get_all_operations.assert_called_once()
    assert result == expected_result


def test_create_operacao_returns_operacao():
    # Arrange
    mock_repo = Mock()
    nome = "Operação X"
    expected_operacao = Operacao(nome=nome)
    mock_repo.create.return_value = expected_operacao
    service = OperacaoService(mock_repo)

    # Act
    result = service.create_operacao(nome)

    # Assert
    mock_repo.create.assert_called_once()
    assert result == expected_operacao
    assert result.nome == nome


def test_find_by_name_returns_true():
    # Arrange
    mock_repo = Mock()
    mock_repo.find_by_name.return_value = True
    service = OperacaoService(mock_repo)

    # Act
    result = service.find_by_name("Operação Y")

    # Assert
    mock_repo.find_by_name.assert_called_once_with("Operação Y")
    assert result is True
