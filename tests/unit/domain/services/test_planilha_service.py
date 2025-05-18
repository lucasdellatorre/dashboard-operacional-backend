from unittest.mock import Mock
from app.domain.services.planilhaservice import PlanilhaService

def test_list_planilhas_calls_repository_and_returns_result():
    # Arrange
    mock_repository = Mock()
    expected_result = ["planilha1", "planilha2"]
    
    mock_repository.get_all_ordered_by_upload_date.return_value = expected_result
    service = PlanilhaService(planilha_repository=mock_repository)

    # Act
    result = service.list_planilhas()

    # Assert
    mock_repository.get_all_ordered_by_upload_date.assert_called_once()
    assert result == expected_result
