from sqlalchemy.orm import Session
from sqlalchemy import func, case, or_, and_, cast, String
from app.domain.repositories.mensagemrepository import IMensagemRepository
from app.infraestructure.database.db import db
from app.domain.entities.mensagem import Mensagem as DomainMensagem
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem
from app.infraestructure.utils.logger import logger

class MensagemRepository(IMensagemRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_mensagens_from_numero_id(self, numero_id: int) -> list[DomainMensagem]:
        results = self.session.query(ORMMensagem).filter(ORMMensagem.numeroId == numero_id).all()
        if results is None:
            return []
        return [ORMMensagem.toMensagemEntidade(result) for result in results]

    def contar_mensagens_por_contato(
        self,
        numeros: list[str],
        tickets: list[str],
        tipo: str,
        grupo: str,
        data_inicial: str,
        data_final: str,
        hora_inicio: str,
        hora_fim: str
    ) -> list[dict]:
        if not numeros:
            return []

        contato_case = case(
            (ORMMensagem.remetente.in_(numeros), ORMMensagem.destinatario),
            (ORMMensagem.destinatario.in_(numeros), ORMMensagem.remetente),
            else_=None
        )

        contato_not_null = or_(
            and_(ORMMensagem.remetente.in_(numeros), ORMMensagem.destinatario.isnot(None)),
            and_(ORMMensagem.destinatario.in_(numeros), ORMMensagem.remetente.isnot(None))
        )

        query = (
            self.session.query(
                contato_case.label("contato"),
                func.count(ORMMensagem.id).label("qtdMensagens")
            )
            .filter(
                or_(
                    ORMMensagem.remetente.in_(numeros),
                    ORMMensagem.destinatario.in_(numeros)
                ),
                contato_not_null
            )
        )

        if tickets:
            query = query.filter(ORMMensagem.internalTicketNumber.in_(tickets))
        
        if grupo and grupo.lower() != "all":
            grupo_lower = grupo.lower()
            if grupo_lower == "group":
                query = query.filter(ORMMensagem.grupoId.isnot(None))
            elif grupo_lower == "number":
                query = query.filter(ORMMensagem.grupoId.is_(None))
            else:
                logger.warning(f"Grupo '{grupo}' não reconhecido. Nenhum filtro aplicado.")

        if tipo and tipo.upper() != "all":
            query = query.filter(ORMMensagem.tipoMensagem == tipo)

        if data_inicial:
            query = query.filter(ORMMensagem.data >= data_inicial)

        if data_final:
            query = query.filter(ORMMensagem.data <= data_final)

        if hora_inicio:
            query = query.filter(ORMMensagem.hora >= hora_inicio)

        if hora_fim:
            query = query.filter(ORMMensagem.hora <= hora_fim)

        query = query.group_by(contato_case)

        resultados = query.all()

        return [{"contato": r.contato, "qtdMensagens": r.qtdMensagens} for r in resultados]