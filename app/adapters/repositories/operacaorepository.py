from sqlalchemy import case, distinct, func
from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.domain.repositories.operacaorepository import IOperacaoRepository
from app.domain.entities.operacao import Operacao as DomainOperacao
from app.adapters.repositories.entities.operacao import Operacao as ORMOperacao
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero as ORMInterceptacaoNumero
from app.adapters.repositories.entities.interceptacao import Interceptacao as ORMInterceptacao

class OperacaoRepository(IOperacaoRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def hasOperacao(self, operacao_id: int) -> bool:
        return self.session.query(ORMOperacao).filter(ORMOperacao.id == operacao_id).first() is not None
    
    def create(self, operacao: DomainOperacao) -> DomainOperacao:
        orm_operacao = ORMOperacao.fromOperacaoEntidade(operacao)
        operacao = self.session.add(orm_operacao)
        self.session.commit()
        return ORMOperacao.toOperacaoEntidade(orm_operacao)
    
    def get_all_operations(self) -> list[DomainOperacao]:
        query = (
        self.session.query(
        ORMOperacao,
        func.count(
        distinct(
        case(
        (ORMInterceptacaoNumero.isAlvo == True, ORMInterceptacaoNumero.numeroId)
        )
        )
        ).label("total_numeros_interceptados")
        )
        .outerjoin(ORMInterceptacao, ORMInterceptacao.operacaoId == ORMOperacao.id)
        .outerjoin(ORMInterceptacaoNumero, ORMInterceptacaoNumero.interceptacaoId == ORMInterceptacao.id)
        .group_by(ORMOperacao.id)
        )
        return query.all()
    
    def find_by_name(self, nome: str) -> DomainOperacao | None:
        result = self.session.query(ORMOperacao).filter(ORMOperacao.nome == nome).first()
        if result is None:
            return None
        return ORMOperacao.toOperacaoEntidade(result)
