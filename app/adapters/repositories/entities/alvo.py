from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Text, String, CHAR
from app.infraestructure.database.db import db
from app.domain.entities.alvo import Alvo as AlvoEntidade

class Alvo(db.Model):
    __tablename__ = "alvos"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    nome = Column(String(255), nullable=True)
    cpf = Column(CHAR(11), nullable=True)
    descricao = Column(Text, nullable=True)
    apelidos = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # Foreign key apontando para Numero.id
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'), nullable=False)
    
    @staticmethod
    def fromAlvoEntidade(alvoEntidade: AlvoEntidade) -> "Alvo":
        """Converts a domain entity to an ORM model instance."""
        return Alvo(**alvoEntidade)
    
    @staticmethod
    def toAlvoEntidade(alvo: "Alvo") -> AlvoEntidade:
        """Converts an ORM model instance to a domain entity."""
        return AlvoEntidade(**alvo)
    
    
