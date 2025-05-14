from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, TIMESTAMP
from app.infraestructure.database.db import db
from app.domain.entities.ligacao import Ligacao as LigacaoEntidade

class Ligacao(db.Model):
    __tablename__ = "ligacoes"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    ligacao_external_id = Column("ligacao_external_id", String, nullable=False)
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    criadorLigacao = Column("criador_ligacao", String, nullable=True)
    tipoLigacao = Column("tipo_ligacao", String, nullable=True)
    criadorIp = Column("criador_ip", String, nullable=True)
    criadorPort = Column("criador_port", String, nullable=True)
    receptor = Column(String, nullable=True)
    receptorIp = Column("receptor_ip", String, nullable=True)
    receptorPort  = Column("receptor_port", String, nullable=True)
    data = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    
    # Foreign key apontando para Numero.id
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'), nullable=False)
    
    @staticmethod
    def fromLigacaoEntidade(ligacaoEntidade: LigacaoEntidade) -> "Ligacao":
        """Converts a domain entity to an ORM model instance."""
        return Ligacao(**ligacaoEntidade)
    
    @staticmethod
    def toLigacaoEntidade(ligacao: "Ligacao") -> LigacaoEntidade:
        """Converts an ORM model instance to a domain entity."""
        return LigacaoEntidade(**ligacao)