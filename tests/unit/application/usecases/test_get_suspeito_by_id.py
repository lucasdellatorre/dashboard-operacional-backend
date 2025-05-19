from unittest.mock import Mock, patch
from app.application.usecases.getsuspeitobyidusecase import GetSuspeitoByIdUseCase

@patch('app.application.dto.suspeitodetalhadodto.SuspeitoDetalhadoDTO.from_entity')
def test_execute_returns_dto_when_entity_found(mock_from_entity):
    # Arrange
    mock_service = Mock()
    id_to_test = 42
    suspeito_entity = Mock()
    mock_service.get_by_id.return_value = suspeito_entity

    expected_dto = Mock()
    mock_from_entity.return_value = expected_dto

    use_case = GetSuspeitoByIdUseCase(mock_service)

    # Act
    result = use_case.execute(id_to_test)

    # Assert
    mock_service.get_by_id.assert_called_once_with(id_to_test)
    mock_from_entity.assert_called_once_with(suspeito_entity)
    assert result == expected_dto

def test_execute_returns_none_when_entity_not_found():
    # Arrange
    mock_service = Mock()
    mock_service.get_by_id.return_value = None

    use_case = GetSuspeitoByIdUseCase(mock_service)

    # Act
    result = use_case.execute(99)

    # Assert
    mock_service.get_by_id.assert_called_once_with(99)
    assert result is None
