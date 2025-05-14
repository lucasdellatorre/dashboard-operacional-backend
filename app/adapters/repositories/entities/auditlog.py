from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, TEXT, TIMESTAMP
from app.infraestructure.database.db import db
from app.domain.entities.numero import Numero as NumeroEntidade

class AuditLog(db.Model):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    tabela = Column(String, nullable=False)
    campo = Column(String, nullable=False)
    valorAntigo = Column("valor_antigo", TEXT, nullable=False)
    valorNovo = Column("valor_novo", TEXT, nullable=False)
    dataAlteracao = Column("data_alteracao", TIMESTAMP, nullable=True, default=datetime.now())
    
    # Foreign key apontando para Numero.id
    usuarioId = Column("usuario_id", Integer, ForeignKey('usuarios.id'), nullable=False)