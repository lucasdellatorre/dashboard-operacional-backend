import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List
from app.infraestructure.database.db import db
from app.domain.entities.mensagem import Mensagem
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem
from app.domain.repositories.mensagemdiarepository import IMensagemDiaRepository
from app.application.dto.filtromensagempordiadto import MensagensDiaSemanaRequestDTO

class MensagemDiaRepository(IMensagemDiaRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def buscar_mensagens_por_dia(self, filtro: MensagensDiaSemanaRequestDTO) -> List[Mensagem]:
        query = self.session.query(ORMMensagem)

        filtros = [
            ORMMensagem.numeroDia == filtro.numero,
            or_(
                ORMMensagem.remetenteDia.in_(filtro.dias),
                ORMMensagem.destinatario.in_(filtro.dias)
            )
        ]

        if filtro.grupo:
            filtros.append(ORMMensagem.grupoDia == filtro.grupo)

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

    def count_mensagens_por_dia(self, filtro):
        query = self.session.query(
            db.extract('dow', ORMMensagem.timestamp).label('dia_semana'),
            func.count().label('quantidade')
        )

        filtros = [
            ORMMensagem.numeroDia == filtro.numero,
            or_(
                ORMMensagem.remetenteDia.in_(filtro.dias),
                ORMMensagem.destinatario.in_(filtro.dias)
            )
        ]

        if filtro.grupo:
            filtros.append(ORMMensagem.grupoDia == filtro.grupo)

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

        resultados = query.filter(and_(*filtros)).group_by('dia_semana').order_by('dia_semana').all()
        return [{"dia": int(dia), "value": int(qtd)} for dia, qtd in resultados]
    
    
    def get_dia_semana_por_data(self, data_str: str) -> str:
        
        dias_semana_map = [
            "domingo", "segunda", "terca", "quarta", "quinta", "sexta", "sabado"
        ]
        data = datetime.datetime.strptime(data_str, "%d/%m/%y")
        dow = (data.weekday() + 1) %7
        return dias_semana_map[dow]


