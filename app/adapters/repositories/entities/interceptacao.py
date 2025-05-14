from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String
from app.infraestructure.database.db import db
from app.domain.entities.interceptacao import Interceptacao as InterceptacaoEntidade

class Interceptacao(db.Model):
    __tablename__ = "interceptacoes"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    
    # Foreign key apontando para operacoes.id
    operacaoId = Column("operacao_id", Integer, ForeignKey('operacoes.id'), nullable=False)
    
    # Foreign key apontando para planilhas.id
    planilhaId = Column("planilha_id", Integer, ForeignKey('planilhas.id'), nullable=False)
    
    @staticmethod
    def fromInterceptacaoEntidade(interceptacaoEntidade: InterceptacaoEntidade) -> "Interceptacao":
        """Converts a domain entity to an ORM model instance."""
        return Interceptacao(**interceptacaoEntidade)
    
    @staticmethod
    def toInterceptacaoEntidade(interceptacao: "Interceptacao") -> InterceptacaoEntidade:
        """Converts an ORM model instance to a domain entity."""
        return InterceptacaoEntidade(**interceptacao)