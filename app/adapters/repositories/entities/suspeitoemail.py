from sqlalchemy import CHAR, Column, ForeignKey, Integer, String, UniqueConstraint
from app.infraestructure.database.db import db

class SuspeitoEmail:
    __tablename__ = "suspeitos_emails"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")    
    suspeitoId = Column("suspeito_id", Integer, ForeignKey('suspeitos.id'), nullable=False)
    email = Column("email", String, nullable=False, primary_key=True)
    lastUpdateDate = Column("last_update_date", String, nullable=True)
    lastupdateCpf = Column("last_update_cpf", CHAR(11), nullable=True)
    
    __table_args__ = (
        UniqueConstraint('suspeito_id', 'email', name='unique_suspeito_email')
    )