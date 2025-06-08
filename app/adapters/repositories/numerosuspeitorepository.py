from sqlalchemy import select
from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.numerosuspeito import NumeroSuspeito
from app.domain.repositories.numerosuspeitorepository import INumeroSuspeitoRepository

class NumeroSuspeitoRepository(INumeroSuspeitoRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def count_by_suspeito(self, suspeito_id: int) -> int:
        return self.session.query(NumeroSuspeito)\
            .filter_by(suspeitoId=suspeito_id)\
            .count()

    def delete_relacao(self, suspeito_id: int, numero_id: int) -> bool:
        relacao = self.session.query(NumeroSuspeito)\
            .filter_by(suspeitoId=suspeito_id, numeroId=numero_id)\
            .first()
        if not relacao:
            return False
        self.session.delete(relacao)
        self.session.commit()
        return True
