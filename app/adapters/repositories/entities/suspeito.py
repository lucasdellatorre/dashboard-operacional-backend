from sqlalchemy import Boolean, Column
from sqlalchemy.types import Integer, Text, String, CHAR
from app.infraestructure.database.db import db
from app.domain.entities.suspeito import Suspeito as SuspeitoEntidade

class Suspeito(db.Model):
    __tablename__ = "suspeitos"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    nome = Column(String(255), nullable=True)
    cpf = Column(CHAR(11), nullable=True)
    anotacoes = Column(Text, nullable=True)
    apelido = Column(String, nullable=True)
    relevante = Column("relevante", Boolean, nullable=True)
    lastUpdateDate = Column("last_update_date", String, nullable=True)
    lastupdateCpf = Column("last_update_cpf", CHAR(11), nullable=True)
    
    @staticmethod
    def fromSuspeitoEntidade(SuspeitoEntidade: SuspeitoEntidade) -> "Suspeito":
        """Converts a domain entity to an ORM model instance."""
        return Suspeito(**SuspeitoEntidade)
    
    @staticmethod
    def toSuspeitoEntidade(Suspeito: "Suspeito") -> SuspeitoEntidade:
        """Converts an ORM model instance to a domain entity."""
        return SuspeitoEntidade(**Suspeito)
    
    @staticmethod
    def toEntity(suspeito: "Suspeito") -> SuspeitoEntidade:
        return SuspeitoEntidade(
        id=suspeito.id,
        internalTicketNumber=suspeito.internalTicketNumber,
        nome=suspeito.nome,
        cpf=suspeito.cpf,
        anotacoes=suspeito.anotacoes,
        apelido=suspeito.apelido,
        relevante=suspeito.relevante,
        lastUpdateDate=suspeito.lastUpdateDate,
        lastUpdateCpf=suspeito.lastupdateCpf
    )
