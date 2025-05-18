from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.domain.repositories.suspeitorepository import ISuspeitoRepositoryInterface
from app.adapters.repositories.entities.suspeito import Suspeito

class SuspeitoRepository(ISuspeitoRepositoryInterface):
    def __init__(self, session: Session = db.session):
        self.session = session

    def atualizar(self, id: int, dados: dict) -> dict:
        suspeito = Suspeito.query.get(id)
        if not suspeito:
            raise LookupError("Suspeito não encontrado.")

        for campo in ['nome', 'cpf', 'apelido', 'anotacoes', 'relevante']:
            if campo in dados:
                setattr(suspeito, campo, dados[campo])

        db.session.commit()

        return suspeito.to_dict()
