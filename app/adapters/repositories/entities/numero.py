from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from app.infraestructure.database.db import db
from app.domain.entities.numero import Numero as NumeroEntidade

class Numero(db.Model):
    __tablename__ = "numeros"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    numero = Column(String, nullable=False)
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    
    @staticmethod
    def fromNumeroEntidade(numeroEntidade: NumeroEntidade) -> "Numero":
        """Converts a domain entity to an ORM model instance."""
        return Numero(**numeroEntidade)
    
    @staticmethod
    def toNumeroEntidade(numero: "Numero") -> NumeroEntidade:
        """Converts an ORM model instance to a domain entity."""
        return NumeroEntidade(id=numero.id, numero=numero.numero, internalTicketNumber=numero.internalTicketNumber)