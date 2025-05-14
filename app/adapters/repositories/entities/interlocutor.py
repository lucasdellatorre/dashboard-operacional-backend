from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from app.infraestructure.database.db import db
from app.domain.entities.interlocutor import Interlocutor as InterlocutorEntidade

class Interlocutor(db.Model):
    __tablename__ = "interlocutores"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    descricao = Column(String, nullable=True)
    nome = Column(String, nullable=True)
    
    # Foreign key apontando para Numero.id
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'), nullable=False)
    
    @staticmethod
    def fromInterlocutorEntidade(interlocutorEntidade: InterlocutorEntidade) -> "Interlocutor":
        """Converts a domain entity to an ORM model instance."""
        return Interlocutor(**interlocutorEntidade)
    
    @staticmethod
    def toInterlocutorEntidade(interlocutor: "Interlocutor") -> InterlocutorEntidade:
        """Converts an ORM model instance to a domain entity."""
        return InterlocutorEntidade(**interlocutor)