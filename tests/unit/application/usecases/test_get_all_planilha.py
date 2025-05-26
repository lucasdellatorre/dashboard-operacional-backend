from datetime import datetime
from unittest.mock import Mock, patch
from app.domain.entities.planilha import Planilha
from app.application.usecases.getallplanilhausecase import GetAllPlanilhaUseCase

@patch('app.application.dto.planilhadto.PlanilhaDTO.fromEntity')
def test_execute_returns_list_of_dtos(mock_from_entity):
    # Arrange
    mock_service = Mock()

    planilha1 = Planilha(id=1, cpf="12345678900", nome="Plan1", dataUpload=datetime(2025, 1, 1), size=32)
    planilha2 = Planilha(id=2, cpf="12345678900", nome="Plan2", dataUpload=datetime(2025, 1, 1), size=32)

    mock_service.list_planilhas.return_value = [planilha1, planilha2]

    dto1 = Mock()
    dto2 = Mock()
    mock_from_entity.side_effect = [dto1, dto2]

    use_case = GetAllPlanilhaUseCase(mock_service)

    # Act
    result = use_case.execute()

    # Assert
    mock_service.list_planilhas.assert_called_once()
    mock_from_entity.assert_any_call(planilha1)
    mock_from_entity.assert_any_call(planilha2)
    assert result == [dto1, dto2]
