from sqlalchemy import Column
from sqlalchemy.types import Integer, String, TIMESTAMP, DATE
from app.infraestructure.database.db import db

class Grupo(db.Model):
    __tablename__ = "grupos"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    internalTicketNumber = Column("internal_ticket_number", String, nullable=False)
    groupExternalId = Column("group_external_id", String, nullable=False)
    dataLocal = Column("data_local", DATE, nullable=False)
    descricao = Column(String, nullable=True)
    horaLocal = Column("hora_local", String, nullable=True)
    tamanho = Column(String, nullable=True)
    assunto = Column(String, nullable=True)
    criado = Column(TIMESTAMP, nullable=False)