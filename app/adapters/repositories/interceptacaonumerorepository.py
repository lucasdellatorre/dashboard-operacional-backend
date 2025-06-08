from app.domain.repositories.interceptacaonumerorepository import IInterceptacaoNumeroRepository
from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.numero import Numero
from app.adapters.repositories.entities.suspeito import Suspeito
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero
from app.adapters.repositories.entities.numerosuspeito import NumeroSuspeito 


class InterceptacaoNumeroRepository(IInterceptacaoNumeroRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def listar_numeros_com_suspeito(self) -> list[dict]:
        query_suspeitos = (
            self.session.query(
                Suspeito.id.label("suspeito_id"),
                Suspeito.apelido.label("apelido"),
                Numero.id.label("numero_id"),
                Numero.numero.label("numero_valor")
            )
            .join(NumeroSuspeito, Suspeito.id == NumeroSuspeito.suspeitoId)
            .join(Numero, Numero.id == NumeroSuspeito.numeroId)
            .distinct(Suspeito.id, Numero.id)
        )

        suspeitos_map: dict[int, dict] = {}
        for row in query_suspeitos.all():
            if row.suspeito_id not in suspeitos_map:
                suspeitos_map[row.suspeito_id] = {
                    "id": row.suspeito_id,
                    "value": row.apelido,
                    "suspect": True,
                    "numeros": []
                }
            suspeitos_map[row.suspeito_id]["numeros"].append({
                "id": row.numero_id,
                "numero": row.numero_valor
            })

        query_anonimos = (
            self.session.query(
                Numero.id.label("id"),
                Numero.numero.label("numero")
            )
            .join(InterceptacaoNumero, InterceptacaoNumero.numeroId == Numero.id)
            .filter(InterceptacaoNumero.isAlvo == True)
            .filter(~Numero.id.in_(
                self.session.query(NumeroSuspeito.numeroId)
            ))
            .distinct(Numero.id)
        )

        anonimos = [
            {
                "id": row.id,
                "value": row.numero,
                "suspect": False,
                "numeros": []
            }
            for row in query_anonimos.all()
        ]

        return list(suspeitos_map.values()) + anonimos


    def get_all_alvos(self) -> list[dict]:
        query = (
            self.session.query(
                Numero.id.label("id"),
                Numero.numero.label("numero")
            )
            .join(InterceptacaoNumero, InterceptacaoNumero.numeroId == Numero.id)
            .filter(InterceptacaoNumero.isAlvo == True)
            .distinct(Numero.id)
        )
        return [dict(row._mapping) for row in query.all()]
    
    def get_alvos_by_interceptacoes(self, tickets: list[str]) -> list[dict]:
        query = (
            self.session.query(
                Numero.id.label("id"),
                Numero.numero.label("numero")
            )
            .join(InterceptacaoNumero, InterceptacaoNumero.numeroId == Numero.id)
            .filter(
                InterceptacaoNumero.interceptacaoId.in_(tickets),
                InterceptacaoNumero.isAlvo == True
            )
            .distinct(Numero.id)
        )
        return [dict(row._mapping) for row in query.all()]