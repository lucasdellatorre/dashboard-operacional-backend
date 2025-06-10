from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship
from app.infraestructure.database.db import db

class NumeroSuspeito(db.Model):
    __tablename__ = "numeros_suspeitos"
    
    numeroId = Column("numero_id", Integer, ForeignKey('numeros.id'), primary_key=True, nullable=False)
    suspeitoId = Column(
        "suspeito_id",
        Integer,
        ForeignKey('suspeitos.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False
    )
    lastUpdateDate = Column("last_update_date", String, nullable=True)
    lastUpdateCpf = Column("last_update_cpf", CHAR(11), nullable=True)

    numero = relationship("Numero", backref="numero_suspeitos", lazy="joined")
    suspeito = relationship(
        "Suspeito",
        back_populates="numero_suspeitos",
        lazy="joined",
        passive_deletes=True
    )
