from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, BOOLEAN
from app.infraestructure.database.db import db

class InterceptacaoNumero(db.Model):
    __tablename__ = "interceptacoes_numeros"
    
    # id = Column(Integer, primary_key=True, autoincrement=True)
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'),nullable=False, primary_key=True)
    interceptacaoId = Column("interceptacao_id", Integer, ForeignKey('interceptacoes.id'),nullable=False, primary_key=True)
    isAlvo = Column("is_alvo", BOOLEAN, nullable=False, default=True)
    relevante = Column(BOOLEAN, nullable=False, default=False)