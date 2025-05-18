from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.numero import Numero as DomainNumero
from app.adapters.repositories.entities.numero import Numero as ORMNumero
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero as ORMInterceptacaoNumero
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.numero import Numero
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero
from app.adapters.repositories.entities.interceptacao import Interceptacao
from app.adapters.repositories.entities.planilha import Planilha
from app.adapters.repositories.entities.operacao import Operacao

class NumeroRepository(INumeroRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def find(self, numero_id) -> DomainNumero:
        result = self.session.query(ORMNumero).get(int(numero_id))
        return ORMNumero.toNumeroEntidade(result)
    
    def isAlvo(self, numero_id) -> bool:
        result = self.session.query(ORMInterceptacaoNumero).filter(ORMInterceptacaoNumero.numeroId == int(numero_id), ORMInterceptacaoNumero.isAlvo == True).first()
        return result is not None
    
    def buscaNumero(self, operacao_ids: list[int]) -> list[dict]:
        query = (
            self.session.query(
                Numero.id.label("id"),
                Numero.numero.label("numero"),
                InterceptacaoNumero.relevante.label("relevante"),
                InterceptacaoNumero.isAlvo.label("isAlvo"),
                Planilha.dataUpload.label("dataUpload")
            )
            .join(InterceptacaoNumero, InterceptacaoNumero.numeroId == Numero.id)
            .join(Interceptacao, Interceptacao.id == InterceptacaoNumero.interceptacaoId)
            .join(Planilha, Planilha.id == Interceptacao.planilhaId)
            .join(Operacao, Operacao.id == Interceptacao.operacaoId)
            .filter(Operacao.id.in_(operacao_ids), InterceptacaoNumero.isAlvo == True)
            .distinct(Numero.id)
        )
        return [dict(row._mapping) for row in query.all()]

    def BuscarOperacoesNumero(self) -> list[dict]:
        query = (
        self.session.query(
            Numero.numero.label("numero"),
            Numero.id.label("numeroId"),
            Operacao.id.label("operacaoId"),
            Operacao.nome.label("nome")
        )
        .join(InterceptacaoNumero, InterceptacaoNumero.numeroId == Numero.id)
        .join(Interceptacao, Interceptacao.id == InterceptacaoNumero.interceptacaoId)
        .join(Operacao, Operacao.id == Interceptacao.operacaoId)
        .filter(InterceptacaoNumero.isAlvo == True)
        .distinct(Numero.id, Operacao.id)
    )

        return [dict(row._mapping) for row in query.all()]
    
    def listar_todos(self) -> list[dict]:
        query = (
            self.session.query(
                ORMNumero.id.label("id"),
                ORMNumero.numero.label("numero")
            )
            .join(ORMInterceptacaoNumero, ORMInterceptacaoNumero.numeroId == ORMNumero.id)
            .distinct(ORMNumero.id)
        )
        resultados = query.all()
        return [dict(row._mapping) for row in resultados]