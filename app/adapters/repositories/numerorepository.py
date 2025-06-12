from sqlalchemy import select
from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.numero import Numero as DomainNumero
from app.adapters.repositories.entities.numero import Numero as ORMNumero
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero as ORMInterceptacaoNumero
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.numero import Numero
from app.adapters.repositories.entities.numerosuspeito import NumeroSuspeito
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero
from app.adapters.repositories.entities.interceptacao import Interceptacao
from app.adapters.repositories.entities.planilha import Planilha
from app.adapters.repositories.entities.operacao import Operacao
from app.adapters.repositories.entities.suspeito import Suspeito

class NumeroRepository(INumeroRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def find(self, numero_id) -> DomainNumero:
        result = self.session.query(ORMNumero).get(int(numero_id))
        return ORMNumero.toNumeroEntidade(result)

    def isNumero(self, numero_id) -> bool:
        result = self.session.query(ORMNumero).get(int(numero_id))
        return result
    
    def isAlvo(self, numero_id) -> bool:
        result = self.session.query(ORMInterceptacaoNumero).filter(ORMInterceptacaoNumero.numeroId == int(numero_id), ORMInterceptacaoNumero.isAlvo == True).first()
        return result is not None
    
    def buscaNumero(self, operacao_ids: list[int]) -> list[dict]:
        
        query_suspeitos = (
            self.session.query(
                Suspeito.id.label("suspeito_id"),
                Suspeito.apelido.label("apelido"),
                InterceptacaoNumero.relevante.label("relevante"),
                Numero.numero.label("numero"),
                Numero.id.label("numero_id"),
                Planilha.dataUpload.label("data_criacao"),
                Operacao.id.label("operacao_id"),
                Operacao.nome.label("operacao_nome")
            )
            .join(NumeroSuspeito, Suspeito.id == NumeroSuspeito.suspeitoId)
            .join(Numero, Numero.id == NumeroSuspeito.numeroId)
            .join(InterceptacaoNumero, InterceptacaoNumero.numeroId == Numero.id)
            .join(Interceptacao, Interceptacao.id == InterceptacaoNumero.interceptacaoId)
            .join(Planilha, Planilha.id == Interceptacao.planilhaId)
            .join(Operacao, Operacao.id == Interceptacao.operacaoId)
            .distinct(Suspeito.id, Numero.id, Operacao.id)
        )
        if operacao_ids:
            query_suspeitos = query_suspeitos.filter(Operacao.id.in_(operacao_ids))

        suspeitos_dict = {}
        for row in query_suspeitos.all():
            sid = row.suspeito_id
            if sid not in suspeitos_dict:
                suspeitos_dict[sid] = {
                    "id": sid,
                    "apelido": row.apelido,
                    "relevante": row.relevante,
                    "operacoes": set(),
                    "numeros": set(),
                    "data_criacao": row.data_criacao.isoformat() if row.data_criacao else None
                }

            suspeitos_dict[sid]["operacoes"].add((row.operacao_id, row.operacao_nome))
            suspeitos_dict[sid]["numeros"].add(row.numero)

        suspeitos = []
        for s in suspeitos_dict.values():
            s["operacoes"] = [
                { "id": op_id, "nome": op_nome }
                for op_id, op_nome in s["operacoes"]
            ]
            s["numeros"] = list(s["numeros"])
            suspeitos.append(s)

        
        subquery_suspeitos = select(NumeroSuspeito.numeroId)

        query_numeros = (
            self.session.query(
                Numero.id.label("id"),
                Numero.numero.label("numero"),
                Operacao.id.label("operacao_id"),
                Operacao.nome.label("operacao_nome")
            )
            .join(InterceptacaoNumero, InterceptacaoNumero.numeroId == Numero.id)
            .join(Interceptacao, Interceptacao.id == InterceptacaoNumero.interceptacaoId)
            .join(Operacao, Operacao.id == Interceptacao.operacaoId)
            .filter(InterceptacaoNumero.isAlvo == True)
            .filter(~Numero.id.in_(subquery_suspeitos))
            .distinct(Numero.id, Operacao.id)
        )
        if operacao_ids:
            query_numeros = query_numeros.filter(Operacao.id.in_(operacao_ids))

        numeros_dict = {}
        for row in query_numeros.all():
            nid = row.id
            if nid not in numeros_dict:
                numeros_dict[nid] = {
                    "id": nid,
                    "numero": row.numero,
                    "operacoes": []
                }
            numeros_dict[nid]["operacoes"].append({
                "id": row.operacao_id,
                "nome": row.operacao_nome
            })

        numeros = list(numeros_dict.values())

        return {
            "suspeitos": suspeitos,
            "numeros": numeros
        }

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

    def listar_com_suspeitos(self) -> list[dict]:
        from app.adapters.repositories.entities.suspeito import Suspeito  # certifique-se de importar corretamente

        query = (
            self.session.query(
                Numero.id.label("id"),
                Numero.numero.label("numero"),
                Suspeito.apelido.label("apelido"),
                (Suspeito.id != None).label("suspeito")
            )
            .outerjoin(NumeroSuspeito, Numero.id == NumeroSuspeito.numeroId)
            .outerjoin(Suspeito, Suspeito.id == NumeroSuspeito.suspeitoId)
            .distinct(Numero.id)
        )

        return [dict(row._mapping) for row in query.all()]

    def get_all_by_ids(self, numero_ids: list[int]) -> list[DomainNumero]:
        if not numero_ids:
            return []

        resultados = (
            self.session.query(ORMNumero)
            .filter(ORMNumero.id.in_(numero_ids))
            .all()
        )

        return [ORMNumero.toNumeroEntidade(numero) for numero in resultados]
