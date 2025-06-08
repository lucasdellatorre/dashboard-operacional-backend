from app.adapters.repositories.entities.interceptacao import Interceptacao as ORMInterceptacao
from app.domain.entities.interceptacao import Interceptacao as InterceptacaoEntity
from app.domain.repositories.interceptacaorepository import IInterceptacaoRepository
from app.infraestructure.database.db import db


class InterceptacaoRepository(IInterceptacaoRepository):
    def get_by_operacao_ids(self, operacao_ids: list[int]) -> list[InterceptacaoEntity]:
        results = (
            db.session.query(ORMInterceptacao)
            .filter(ORMInterceptacao.operacaoId.in_(operacao_ids))
            .all()
        )
        
        return [
            InterceptacaoEntity(
                id=orm.id,
                internalTicketNumber=orm.internalTicketNumber,
                operacaoId=orm.operacaoId,
                planilhaId=orm.planilhaId
            )
            for orm in results
        ]
