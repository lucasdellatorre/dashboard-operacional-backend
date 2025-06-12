# from unittest.mock import Mock
# from app.application.usecases.teiaipmessagecountusecase import TeiaIPMessageCountUseCase
# from app.application.dto.teiaipmessagecountdto import TeiaIPMessageCountRequestDTO, NumeroMessageCountResponseDTO
# from app.domain.entities.ip import IP

# def test_execute_builds_nodes_and_links_for_ips():
#     # Arrange
#     mock_ip_service = Mock()
#     mock_mensagem_service = Mock()

#     request = TeiaIPMessageCountRequestDTO(ip_ids=[1, 2])

#     ip1 = IP(
#         id=1,
#         internalTicketNumber="ticket-001",
#         ip="192.168.0.1",
#         versao="v1",
#         numeroId=10
#     )
#     ip2 = IP(
#         id=2,
#         internalTicketNumber="ticket-002",
#         ip="10.0.0.1",
#         versao="v1",
#         numeroId=11
#     )

#     mock_ip_service.find.side_effect = [[ip1], [ip2]]

#     mock_mensagem_service.count_mensagens_por_ip.side_effect = [
#         {"5511999999999": 4},
#         {"5511888888888": 2}
#     ]

#     use_case = TeiaIPMessageCountUseCase(
#         teia_ip_service=mock_ip_service,
#         mensagem_service=mock_mensagem_service
#     )

#     # Act
#     result = use_case.execute(request)

#     # Assert
#     mock_ip_service.find.assert_any_call([1])
#     mock_ip_service.find.assert_any_call([2])
#     mock_mensagem_service.count_mensagens_por_ip.assert_any_call(ip1)
#     mock_mensagem_service.count_mensagens_por_ip.assert_any_call(ip2)

#     expected_nodes = [
#         {"id": "192.168.0.1", "group": 3},
#         {"id": "5511999999999", "group": 7},
#         {"id": "10.0.0.1", "group": 3},
#         {"id": "5511888888888", "group": 7}
#     ]

#     expected_links = [
#         {"source": "192.168.0.1", "target": "5511999999999", "value": 4},
#         {"source": "10.0.0.1", "target": "5511888888888", "value": 2}
#     ]

#     assert isinstance(result, NumeroMessageCountResponseDTO)
#     assert sorted(result.nodes, key=lambda x: x["id"]) == sorted(expected_nodes, key=lambda x: x["id"])
#     assert sorted(result.links, key=lambda x: (x["source"], x["target"])) == sorted(expected_links, key=lambda x: (x["source"], x["target"]))
