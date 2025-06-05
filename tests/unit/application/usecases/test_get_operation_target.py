# from unittest.mock import Mock, patch
# from app.application.usecases.getoperationtargetsusecase import GetOperationTargetsUseCase

# @patch('app.application.dto.listanumerodto.ListaNumeroDTO.from_dict')
# def test_execute_returns_list_of_dtos(mock_from_dict):
#     # Arrange
#     mock_service = Mock()
#     operacao_ids = [1, 2, 3]

#     rows = [
#         {'numeroId': 1, 'numero': '123', 'relevante': True, 'isAlvo': True, 'dataUpload': '2024-01-01', 'operacoes': []},
#         {'numeroId': 2, 'numero': '456', 'relevante': False, 'isAlvo': False, 'dataUpload': '2024-01-02', 'operacoes': []}
#     ]
#     mock_service.listarNumeroOperacao.return_value = rows

#     dto1 = Mock()
#     dto2 = Mock()
#     mock_from_dict.side_effect = [dto1, dto2]

#     use_case = GetOperationTargetsUseCase(mock_service)

#     # Act
#     result = use_case.execute(operacao_ids)

#     # Assert
#     mock_service.listarNumeroOperacao.assert_called_once_with(operacao_ids)
#     mock_from_dict.assert_any_call(rows[0])
#     mock_from_dict.assert_any_call(rows[1])
#     assert result == [dto1, dto2]
