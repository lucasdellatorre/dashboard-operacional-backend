from datetime import datetime
from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, UniqueConstraint
from app.infraestructure.database.db import db
from app.domain.entities.suspeitoemail import SuspeitoEmail as SuspeitoEmailEntidade

class SuspeitoEmail(db.Model):
    __tablename__ = "suspeitos_emails"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    suspeitoId = Column("suspeito_id", Integer, ForeignKey('suspeitos.id'), nullable=False)
    email = Column("email", String, nullable=False)
    lastUpdateDate = Column("last_update_date", String, nullable=True, default=datetime.now())
    lastUpdateCpf = Column("last_update_cpf", CHAR(11), nullable=True)

    __table_args__ = (
        UniqueConstraint('suspeito_id', 'email', name='unique_suspeito_email'),
    )
    
    @staticmethod
    def fromSuspeitoEmailEntidade(suspeitoEmail: SuspeitoEmailEntidade) -> "SuspeitoEmail":
        """Converts a domain entity to an ORM model instance."""
        return SuspeitoEmail(suspeitoId=suspeitoEmail.suspeitoId, email=suspeitoEmail.email, lastUpdateCpf=suspeitoEmail.lastUpdateCpf)
    
    @staticmethod
    def toSuspeitoEmailEntidade(suspeitoEmail: "SuspeitoEmail") -> SuspeitoEmailEntidade:
        """Converts an ORM model instance to a domain entity."""
        return SuspeitoEmailEntidade(id=suspeitoEmail.id, suspeitoId=suspeitoEmail.suspeitoId, email=suspeitoEmail.email, lastUpdateCpf=suspeitoEmail.lastUpdateCpf, lastUpdateDate=suspeitoEmail.lastUpdateDate)