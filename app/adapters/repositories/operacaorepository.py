from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.domain.repositories.operacaorepository import IOperacaoRepository
from app.domain.entities.operacao import Operacao as DomainOperacao
from app.adapters.repositories.entities.operacao import Operacao as ORMOperacao

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
        orm_operacoes = self.session.query(ORMOperacao).all()
        if len(orm_operacoes) == 0:
            return []
        return [ORMOperacao.toOperacaoEntidade(orm_operacao) for orm_operacao in orm_operacoes]
    
    def find_by_name(self, nome: str) -> DomainOperacao | None:
        result = self.session.query(ORMOperacao).filter(ORMOperacao.nome == nome).first()
        if result is None:
            return None
        return ORMOperacao.toOperacaoEntidade(result)
