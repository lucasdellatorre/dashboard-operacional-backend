# from unittest.mock import Mock, patch
# from datetime import datetime
# from app.domain.entities.ip import IP
# from app.application.usecases.getallipusecase import GetAllIPUseCase


# @patch('app.application.dto.ipdto.IPDTO.fromEntity')
# def test_execute_returns_sorted_ip_dtos(mock_from_entity):
#     # Arrange
#     mock_service = Mock()

#     ip1 = IP(id=1, internalTicketNumber="ABCDE", versao="ipv4", ip="192.168.0.1", numeroId=1, timestamp=datetime(2025, 5, 1))
#     ip2 = IP(id=2, internalTicketNumber="ABCDE", versao="ipv4", ip="10.0.0.1", numeroId=1, timestamp=datetime(2025, 5, 2))

#     mock_service.list_ips.return_value = [ip1, ip2]

#     mock_dto1 = Mock()
#     mock_dto2 = Mock()
#     mock_from_entity.side_effect = [mock_dto2, mock_dto1]

#     use_case = GetAllIPUseCase(mock_service)

#     # Act
#     result = use_case.execute()

#     # Assert
#     mock_service.list_ips.assert_called_once()
#     mock_from_entity.assert_any_call(ip2)
#     mock_from_entity.assert_any_call(ip1)
#     assert result == [mock_dto2, mock_dto1]
