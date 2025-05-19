from datetime import datetime
from unittest.mock import Mock, patch, ANY
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

@patch('app.domain.services.operacaoservice.OperacaoComAlvosDTO')
def test_get_all_operacoes_returns_list(mock_dto_class):
    # Arrange
    mock_repo = Mock()

    orm_operacao = Mock()
    orm_operacao.id = 1
    orm_operacao.nome = "Operação Teste"
    orm_operacao.dataCriacao = datetime(2024, 1, 1)

    mock_repo.get_all_operations.return_value = [(orm_operacao, 5)]

    # Mock DTO.fromEntity return
    mock_dto_instance = Mock()
    mock_dto_class.fromEntity.return_value = mock_dto_instance

    service = OperacaoService(mock_repo)

    # Act
    result = service.get_all_operacoes()

    # Assert
    mock_repo.get_all_operations.assert_called_once()
    mock_dto_class.fromEntity.assert_called_once_with(
        operacao=ANY,
        qtd_alvos=5
    )
    assert result == [mock_dto_instance]


def test_create_operacao_returns_operacao():
    # Arrange
    mock_repo = Mock()
    nome = "Operação X"
    dataCriacao = datetime(2024, 1, 1)
    expected_operacao = Operacao(nome=nome, dataCriacao=dataCriacao)
    mock_repo.create.return_value = expected_operacao
    service = OperacaoService(mock_repo)

    # Act
    result = service.create_operacao(nome)

    # Assert
    mock_repo.create.assert_called_once()
    assert result == expected_operacao
    assert result.nome == nome
    assert result.dataCriacao == dataCriacao


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
