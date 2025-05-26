from unittest.mock import Mock
from app.domain.services.mensagemservice import MensagemService
from app.domain.entities.numero import Numero

class FakeMensagem:
    def __init__(self, remetente, destinatario):
        self.remetente = remetente
        self.destinatario = destinatario

def test_count_mensagens_por_alvo_correctly_counts_messages():
    # Arrange
    mock_repo = Mock()
    numero = Numero(id=1, numero="5555")
    mensagens = [
        FakeMensagem(remetente="5555", destinatario="1234"),  # 5555 -> 1234
        FakeMensagem(remetente="5555", destinatario="1234"),  # 5555 -> 1234
        FakeMensagem(remetente="5678", destinatario="5555"),  # 5678 -> 5555
        FakeMensagem(remetente="9999", destinatario="0000"),  # unrelated
    ]
    mock_repo.get_mensagens_from_numero_id.return_value = mensagens
    service = MensagemService(mock_repo)

    # Act
    result = service.count_mensagens_por_alvo(numero)

    # Assert
    mock_repo.get_mensagens_from_numero_id.assert_called_once_with(1)
    assert result == {
        "1234": 2,
        "5678": 1
    }
