from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from app.infraestructure.database.db import db
from app.domain.entities.mensagem import Mensagem
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem
from app.domain.repositories.mensagemrepository import IMensagemRepository

class MensagensRepository(IMensagemRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def buscar_por_filtros(self, filtro: Mensagem) -> List[Mensagem]:
        query = self.session.query(ORMMensagem)

        filtros = [
            ORMMensagem.numeroId == filtro.numero,
            or_(
                ORMMensagem.remetenteIp.in_(filtro.ips),
                ORMMensagem.destinatario.in_(filtro.ips)
            )
        ]

        if filtro.grupo:
            filtros.append(ORMMensagem.grupoId == filtro.grupo)

        if filtro.tipo:
            filtros.append(ORMMensagem.tipoMensagem == filtro.tipo)

        if filtro.data_inicial:
            filtros.append(ORMMensagem.data >= filtro.data_inicial)
        if filtro.data_final:
            filtros.append(ORMMensagem.data <= filtro.data_final)

        if filtro.hora_inicial:
            filtros.append(ORMMensagem.hora >= filtro.hora_inicial)
        if filtro.hora_final:
            filtros.append(ORMMensagem.hora <= filtro.hora_final)

        if filtro.dias_semana:
            filtros.append(
                db.extract('dow', ORMMensagem.timestamp).in_(filtro.dias_semana)
            )

        resultados = query.filter(and_(*filtros)).all()

        return [ORMMensagem.toMensagemEntidade(m) for m in resultados]

