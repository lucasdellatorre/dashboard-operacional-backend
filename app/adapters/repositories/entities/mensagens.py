from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, TIMESTAMP
from app.infraestructure.database.db import db
from app.domain.entities.mensagem import Mensagem as MensagemEntidade

class Mensagem(db.Model):
    __tablename__ = "mensagens"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    messageExternalId = Column("message_external_id", String, nullable=True)
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    grupoId = Column("grupo_id", String, nullable=True)
    remetente = Column(String, nullable=True)
    remetenteIp = Column("remetente_ip", String, nullable=True)
    remetenteDispositivo = Column("remetente_dispositivo", String, nullable=True)
    tipoMensagem = Column("tipo_mensagem", String, nullable=True)
    estiloMensagem = Column("estilo_mensagem", String, nullable=True)
    tamanhoMensagem = Column("tamanho_mensagem", String, nullable=True)
    remetentePorta = Column("remetente_porta", String, nullable=True)
    data = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    destinatario = Column(String, nullable=True)
    
    # Foreign key apontando para Numero.id
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'), nullable=False)
    
    @staticmethod
    def fromMensagemEntidade(mensagemEntidade: MensagemEntidade) -> "Mensagem":
        """Converts a domain entity to an ORM model instance."""
        return Mensagem(**mensagemEntidade)
    
    @staticmethod
    def toMensagemEntidade(mensagem: "Mensagem") -> MensagemEntidade:
        """Converts an ORM model instance to a domain entity."""
        
        return MensagemEntidade(
	    id=mensagem.id,
	    messageExternalId=mensagem.messageExternalId,
	    internalTicketNumber=mensagem.internalTicketNumber,
	    grupoId=mensagem.grupoId,
	    numeroId=mensagem.numeroId,
	    remetente=mensagem.remetente,
	    remetenteIp=mensagem.remetenteIp,
	    remetenteDispositivo=mensagem.remetenteDispositivo,
	    tipoMensagem=mensagem.tipoMensagem,
	    estiloMensagem=mensagem.estiloMensagem,
	    tamanhoMensagem=mensagem.tamanhoMensagem,
	    data=mensagem.data,
	    hora=mensagem.hora,
	    timestamp=mensagem.timestamp,
	    destinatario=mensagem.destinatario,
	    remetentePorta=mensagem.remetentePorta
	)
