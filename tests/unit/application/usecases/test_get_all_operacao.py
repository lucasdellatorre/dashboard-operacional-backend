from unittest.mock import Mock
from app.application.usecases.getalloperacaousecase import GetAllOperacaoUseCase
from app.application.dto.operacaocomalvosdto import OperacaoComAlvosDTO

def test_execute_returns_all_operacoes():
    # Arrange
    mock_service = Mock()
    
    dto1 = OperacaoComAlvosDTO(nome="Op1", id=1, qtd_alvos=3)
    dto2 = OperacaoComAlvosDTO(nome="Op2", id=2, qtd_alvos=5)
    expected_operacoes = [dto1, dto2]
    
    mock_service.get_all_operacoes.return_value = expected_operacoes
    
    use_case = GetAllOperacaoUseCase(mock_service)
    
    # Act
    result = use_case.execute()
    
    # Assert
    mock_service.get_all_operacoes.assert_called_once()
    assert result == expected_operacoes