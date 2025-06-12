# from unittest.mock import Mock
# from app.application.usecases.teiamessagecount import TeiaMessageCountUseCase
# from app.application.dto.numeromessagecountdto import NumeroMessageCountRequestDTO, NumeroMessageCountResponseDTO
# from app.domain.entities.numero import Numero

# def test_execute_builds_nodes_and_links():
#     # Arrange
#     mock_numero_service = Mock()
#     mock_mensagem_service = Mock()

#     request = NumeroMessageCountRequestDTO(numeros=[1, 2])

#     numero1 = Numero(id=1, numero="1111")
#     numero2 = Numero(id=2, numero="2222")
#     mock_numero_service.find.side_effect = [numero1, numero2]

#     mock_numero_service.isAlvo.side_effect = [True, False]

#     # Setup mensagem_service.count_mensagens_por_alvo only called for alvo (numero1)
#     mock_mensagem_service.count_mensagens_por_alvo.return_value = {
#         "3333": 5,
#         "4444": 10
#     }

#     use_case = TeiaMessageCountUseCase(mock_numero_service, mock_mensagem_service)

#     # Act
#     result = use_case.execute(request)

#     # Assert
#     mock_numero_service.find.assert_any_call(1)
#     mock_numero_service.find.assert_any_call(2)

#     mock_numero_service.isAlvo.assert_any_call(1)
#     mock_numero_service.isAlvo.assert_any_call(2)

#     # Check count_mensagens_por_alvo called only once for alvo number1
#     mock_mensagem_service.count_mensagens_por_alvo.assert_called_once_with(numero1)

#     expected_nodes = [
#         {"id": "1111", "group": 3},
#         {"id": "2222", "group": 7}
#     ]

#     expected_links = [
#         {"source": "1111", "target": "3333", "value": 5},
#         {"source": "1111", "target": "4444", "value": 10}
#     ]

#     # Result should be the response DTO with these nodes and links
#     assert isinstance(result, NumeroMessageCountResponseDTO)
#     assert result.nodes == expected_nodes
#     assert result.links == expected_links
