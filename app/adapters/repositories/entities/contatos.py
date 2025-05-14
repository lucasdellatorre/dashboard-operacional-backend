from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, BOOLEAN
from app.infraestructure.database.db import db
from app.domain.entities.contato import Contato as ContatoEntidade

class Contato(db.Model):
    __tablename__ = "contatos"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    tipoContato = Column("tipo_contato", BOOLEAN, nullable=False)
    numeroContatoId = Column("numero_contato_id", Integer, ForeignKey('numeros.id'), nullable=False)
    
    # Foreign key apontando para Numero.id
    numeroOrigemId = Column("numero_origem_id", Integer, ForeignKey('numeros.id'), nullable=False)
    
    @staticmethod
    def fromContatoEntidade(contatoEntidade: ContatoEntidade) -> "Contato":
        """Converts a domain entity to an ORM model instance."""
        return Contato(**contatoEntidade)
    
    @staticmethod
    def toContatoEntidade(contato: "Contato") -> ContatoEntidade:
        """Converts an ORM model instance to a domain entity."""
        return ContatoEntidade(**contato)