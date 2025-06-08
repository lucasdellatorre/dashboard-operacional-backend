from sqlalchemy import Column, Integer, String, CHAR, Text, Boolean
from sqlalchemy.orm import relationship
from app.infraestructure.database.db import db
from app.domain.entities.suspeito import Suspeito as SuspeitoEntidade

class Suspeito(db.Model):
    __tablename__ = "suspeitos"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    nome = Column(String(255), nullable=True)
    cpf = Column(CHAR(11), nullable=True)
    anotacoes = Column(Text, nullable=True)
    apelido = Column(String, nullable=True)
    relevante = Column("relevante", Boolean, nullable=True)
    lastUpdateDate = Column("last_update_date", String, nullable=True)
    lastUpdateCpf = Column("last_update_cpf", CHAR(11), nullable=True)

    emails = relationship(
        "SuspeitoEmail",
        backref="suspeito",
        lazy="joined",
        cascade="all, delete-orphan"
    )

    numero_suspeitos = relationship(
        "NumeroSuspeito",
        back_populates="suspeito",
        lazy="joined",
        cascade="all, delete-orphan"
    )
    
    @staticmethod
    def fromSuspeitoEntidade(SuspeitoEntidade: SuspeitoEntidade) -> "Suspeito":
        return Suspeito(**SuspeitoEntidade)

    @staticmethod
    def toSuspeitoEntidade(Suspeito: "Suspeito") -> SuspeitoEntidade:
        return SuspeitoEntidade(**Suspeito)
    
    @staticmethod
    def toEntity(suspeito: "Suspeito") -> SuspeitoEntidade:
        return SuspeitoEntidade(
        id=suspeito.id,
        nome=suspeito.nome,
        cpf=suspeito.cpf,
        anotacoes=suspeito.anotacoes,
        apelido=suspeito.apelido,
        relevante=suspeito.relevante,
        lastUpdateDate=suspeito.lastUpdateDate,
        lastUpdateCpf=suspeito.lastUpdateCpf
    )
