from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, TIMESTAMP, DATE, TIME
from app.infraestructure.database.db import db
from app.domain.entities.ip import IP as IpEntidade

class IP(db.Model):
    __tablename__ = "ips"

    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    ip = Column(String, nullable=False)
    versao = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    data = Column(DATE, nullable=False)
    hora = Column(TIME, nullable=False)
    
    # Foreign key apontando para Numero.id
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'), nullable=False)
    
    @staticmethod
    def fromIpEntidade(ipEntidade: IpEntidade) -> "IP":
        """Converts a domain entity to an ORM model instance."""
        return IP(**ipEntidade)
    
    @staticmethod
    def toIpEntidade(ip: "IP") -> IpEntidade:
        """Converts an ORM model instance to a domain entity."""
        return IpEntidade(**ip)
    
    