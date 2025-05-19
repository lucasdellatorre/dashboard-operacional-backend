from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from app.infraestructure.database.db import db
from app.domain.entities.operacao import Operacao as OperacaoEntidade

class Operacao(db.Model):
    __tablename__ = "operacoes"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    nome = Column(String, nullable=True)
    dataCriacao = Column("data_criacao", String, nullable=True)
    
    def __repr__(self):
        return f"Operacao(id={self.id} nome={self.nome} dataCriacao={self.dataCriacao})"
    
    @staticmethod
    def fromOperacaoEntidade(operacaoEntidade: OperacaoEntidade) -> "Operacao":
        """Converts a domain entity to an ORM model instance."""
        return Operacao(id=operacaoEntidade.id, nome=operacaoEntidade.nome, dataCriacao=operacaoEntidade.dataCriacao)
    
    @staticmethod
    def toOperacaoEntidade(operacao: "Operacao") -> OperacaoEntidade:
        """Converts an ORM model instance to a domain entity."""
        return OperacaoEntidade(id=operacao.id, nome=operacao.nome, dataCriacao=operacao.dataCriacao)