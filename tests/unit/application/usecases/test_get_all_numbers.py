from unittest.mock import Mock
from app.application.usecases.getallnumbersusecase import GetAllNumbersUseCase


def test_execute_returns_all_numbers():
    # Arrange
    mock_service = Mock()
    expected_result = [
        {"id": 1, "numero": "123456789"},
        {"id": 2, "numero": "987654321"}
    ]
    mock_service.listar_numeros.return_value = expected_result

    use_case = GetAllNumbersUseCase(mock_service)

    # Act
    result = use_case.execute()

    # Assert
    mock_service.listar_numeros.assert_called_once()
    assert result == expected_result
