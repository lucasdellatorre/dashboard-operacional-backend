from sqlalchemy.orm import Session
from sqlalchemy import func, case, or_
from app.infraestructure.database.db import db
from app.domain.entities.mensagem import Mensagem as DomainMensagem
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem

class MensagemRepository:
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_mensagens_from_numero_id(self, numero_id: int) -> list[DomainMensagem]:
        results = self.session.query(ORMMensagem).filter(ORMMensagem.numeroId == numero_id).all()
        if results is None:
            return []
        return [ORMMensagem.toMensagemEntidade(result) for result in results]

    def contar_mensagens_por_contato(self, numero_ids: list[int]) -> list[dict]:
        """
        Recebe uma lista de ids de números e retorna uma lista de dicts:
        {
            "contato": str,
            "qtdMensagens": int
        }
        Considera mensagens onde o número é remetente (numeroId) ou destinatário (destinatario).
        """
        if not numero_ids:
            return []

        # Converte para string para comparar com destinatario (que é string)
        numero_ids_str = [str(n) for n in numero_ids]

        contato_case = case(
            [
                (ORMMensagem.numeroId.in_(numero_ids), ORMMensagem.destinatario),
                (ORMMensagem.destinatario.in_(numero_ids_str), ORMMensagem.remetente)
            ]
        )

        query = (
            self.session.query(
                contato_case.label("contato"),
                func.count(ORMMensagem.id).label("qtdMensagens")
            )
            .filter(
                or_(
                    ORMMensagem.numeroId.in_(numero_ids),
                    ORMMensagem.destinatario.in_(numero_ids_str)
                )
            )
            .group_by(contato_case)
        )

        resultados = query.all()

        return [{"contato": r.contato, "qtdMensagens": r.qtdMensagens} for r in resultados]
