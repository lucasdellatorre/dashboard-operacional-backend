from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, UniqueConstraint
from app.infraestructure.database.db import db

class SuspeitoEmail(db.Model):
    __tablename__ = "suspeitos_emails"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    suspeitoId = Column("suspeito_id", Integer, ForeignKey('suspeitos.id'), nullable=False)
    email = Column("email", String, nullable=False)
    lastUpdateDate = Column("last_update_date", String, nullable=True)
    lastUpdateCpf = Column("last_update_cpf", CHAR(11), nullable=True)

    __table_args__ = (
        UniqueConstraint('suspeito_id', 'email', name='unique_suspeito_email'),
    )
