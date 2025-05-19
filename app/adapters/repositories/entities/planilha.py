from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.types import Integer,  String, DATE
from app.infraestructure.database.db import db
from app.domain.entities.planilha import Planilha as PlanilhaEntidade

class Planilha(db.Model):
    __tablename__ = "planilhas"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    nome = Column(String, nullable=False)
    dataUpload = Column("data_upload", DATE, nullable=False, default=datetime.now())
    size = Column(Integer, nullable=False)
    cpf = Column(String(11), nullable=True)
    
    @staticmethod
    def fromPlanilhaEntidade(planilha: PlanilhaEntidade) -> "Planilha":
        """Converts a domain entity to an ORM model instance."""
        return Planilha(**planilha)
    
    @staticmethod
    def toPlanilhaEntidade(planilha: "Planilha") -> PlanilhaEntidade:
        """Converts an ORM model instance to a domain entity."""
        return PlanilhaEntidade(**planilha)
