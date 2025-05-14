from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from app.infraestructure.database.db import db

class GrupoNumero(db.Model):
    __tablename__ = "grupos_numeros"
    
    grupoId = Column("grupo_id", Integer, ForeignKey('grupos.id'), primary_key=True)
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'), primary_key=True)