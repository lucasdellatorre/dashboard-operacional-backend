from unittest.mock import Mock
from app.application.usecases.getalltargetnumbersusecase import GetAllTargetNumbersUseCase
from app.application.dto.numerosimplesdto import NumeroSimplesDTO

def test_execute_show_suspects_true():
    # Arrange
    mock_interceptacao_service = Mock()
    mock_suspeito_service = Mock()

    # Data returned when showing suspects
    mock_interceptacao_service.listar_numeros_com_suspeito_e_numeros.return_value = [
        {"id": 1, "value": "12345", "suspect": True, "numeros": ["num1", "num2"]},
        {"id": 2, "value": "67890", "suspect": False, "numeros": []}
    ]

    use_case = GetAllTargetNumbersUseCase(mock_interceptacao_service, mock_suspeito_service)

    # Act
    result = use_case.execute(show_suspects=True)

    # Assert
    mock_interceptacao_service.listar_numeros_com_suspeito_e_numeros.assert_called_once()
    assert len(result) == 2
    assert all(isinstance(r, NumeroSimplesDTO) for r in result)
    assert result[0].id == 1
    assert result[0].value == "12345"
    assert result[0].suspect is True
    assert result[0].numeros == ["num1", "num2"]

def test_execute_show_suspects_false():
    # Arrange
    mock_interceptacao_service = Mock()
    mock_suspeito_service = Mock()

    # Data returned when not showing suspects
    mock_interceptacao_service.get_all_numeros.return_value = [
        {"id": 10, "numero": "54321"},
        {"id": 20, "numero": "09876"}
    ]

    use_case = GetAllTargetNumbersUseCase(mock_interceptacao_service, mock_suspeito_service)

    # Act
    result = use_case.execute(show_suspects=False)

    # Assert
    mock_interceptacao_service.get_all_numeros.assert_called_once()
    assert len(result) == 2
    assert all(isinstance(r, NumeroSimplesDTO) for r in result)
    assert result[0].id == 10
    assert result[0].value == "54321"
    assert result[0].suspect is False
    assert result[0].numeros == []
