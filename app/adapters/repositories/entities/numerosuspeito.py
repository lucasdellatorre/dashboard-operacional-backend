from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.types import Integer
from app.infraestructure.database.db import db

class NumeroSuspeito(db.Model):
    __tablename__ = "numeros_suspeitos"
    
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'),nullable=False, primary_key=True)
    suspeitoId = Column("suspeito_id", Integer, ForeignKey('suspeitos.id'),nullable=False, primary_key=True)
    lastUpdateDate = Column("last_update_date", String, nullable=True)
    lastupdateCpf = Column("last_update_cpf", CHAR(11), nullable=True)