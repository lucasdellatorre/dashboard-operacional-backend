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
        subquery = (
            self.session.query(
                NumeroSuspeito.numeroId.label("numero_id"),
                Suspeito.id.label("suspeito_id"),
                Suspeito.apelido.label("apelido")
            )
            .join(Suspeito, Suspeito.id == NumeroSuspeito.suspeitoId)
            .subquery()
        )

        query = (
            self.session.query(
                InterceptacaoNumero.numeroId.label("numero_id"),
                Numero.numero.label("numero_valor"),
                subquery.c.apelido,
                subquery.c.suspeito_id,
                Numero.id.label("numero_id_real")  # redundante, mas claro
            )
            .join(Numero, Numero.id == InterceptacaoNumero.numeroId)
            .outerjoin(subquery, InterceptacaoNumero.numeroId == subquery.c.numero_id)
            .filter(InterceptacaoNumero.isAlvo == True)
            .distinct(InterceptacaoNumero.numeroId)
        )

        rows = query.all()

        resultados: list[dict] = []
        suspeitos_map: dict[int, dict] = {}
        anonimos: list[dict] = []

        for row in rows:
            if row.suspeito_id:
                if row.suspeito_id not in suspeitos_map:
                    suspeitos_map[row.suspeito_id] = {
                        "id": row.suspeito_id,
                        "value": row.apelido,
                        "suspect": True,
                        "numeros": []
                    }

                suspeitos_map[row.suspeito_id]["numeros"].append({
                    "id": row.numero_id_real,
                    "numero": row.numero_valor
                })

            else:
                anonimos.append({
                    "id": row.numero_id_real,
                    "value": row.numero_valor,
                    "suspect": False,
                    "numeros": []
                })

        resultados.extend(suspeitos_map.values())
        resultados.extend(anonimos)
        return resultados


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