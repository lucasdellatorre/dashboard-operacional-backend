from datetime import datetime
from typing import List, Optional
from app.domain.entities.mensagem import Mensagem


class MensagemResponseDTO:
    def __init__(self, mensagem: Mensagem):
        self.id = mensagem.id
        self.message_external_id = mensagem.messageExternalId
        self.internal_ticket_number = mensagem.internalTicketNumber
        self.grupo_id = mensagem.grupoId
        self.numero_id = mensagem.numeroId
        self.remetente = mensagem.remetente
        self.remetente_ip = mensagem.remetenteIp
        self.remetente_dispositivo = mensagem.remetenteDispositivo
        self.tipo_mensagem = mensagem.tipoMensagem
        self.estilo_mensagem = mensagem.estiloMensagem
        self.tamanho_mensagem = mensagem.tamanhoMensagem
        self.data = mensagem.data
        self.hora = mensagem.hora
        self.timestamp = (
            mensagem.timestamp.isoformat() if mensagem.timestamp else None
        )
        self.destinatario = mensagem.destinatario
        self.remetente_porta = mensagem.remetentePorta

    def to_dict(self):
        return {
            "id": self.id,
            "message_external_id": self.message_external_id,
            "internal_ticket_number": self.internal_ticket_number,
            "grupo_id": self.grupo_id,
            "numero_id": self.numero_id,
            "remetente": self.remetente,
            "remetente_ip": self.remetente_ip,
            "remetente_dispositivo": self.remetente_dispositivo,
            "tipo_mensagem": self.tipo_mensagem,
            "estilo_mensagem": self.estilo_mensagem,
            "tamanho_mensagem": self.tamanho_mensagem,
            "data": self.data,
            "hora": self.hora,
            "timestamp": self.timestamp,
            "destinatario": self.destinatario,
            "remetente_porta": self.remetente_porta,
        }