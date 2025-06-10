from venv import logger
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_
from typing import List
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem
from app.domain.repositories.mensagemiprepository import IMensagemIPRepository
from app.application.dto.filtromensagemdto import FiltroMensagemDTO
from app.application.dto.mensagemporipresponsedto import MensagemPorIpResponseDTO

class MensagemIPRepository(IMensagemIPRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def buscar_mensagens_por_ip(self, filtro: FiltroMensagemDTO, tickets: list[str]) -> List[MensagemPorIpResponseDTO]:
        numeros = list(filtro.numero or [])
        
        query = ( 
              self.session
              .query(
                    ORMMensagem.remetenteIp.label("ip"),
                    func.count(ORMMensagem.id).label("quantidade_mensagens"),
              )
              .filter(ORMMensagem.numeroId.in_(numeros))
              )
        if tickets:
            query = query.filter(ORMMensagem.internalTicketNumber.in_(tickets))
        else:
            return []
        
        if filtro.grupo and filtro.grupo.lower() != "all":
            grupo_lower = filtro.grupo.lower()
            if grupo_lower == "group":
                query = query.filter(ORMMensagem.grupoId.isnot(None))
            elif grupo_lower == "number":
                query = query.filter(ORMMensagem.grupoId.is_(None))
            else:
                logger.warning(f"Grupo '{filtro.grupo}' não reconhecido. Nenhum filtro aplicado.")

        if filtro.tipo and filtro.tipo.upper() != "ALL":
            query = query.filter(ORMMensagem.tipoMensagem == filtro.tipo)

        if filtro.data_inicial:
            query = query.filter(ORMMensagem.data >= filtro.data_inicial)

        if filtro.data_final:
            query = query.filter(ORMMensagem.data <= filtro.data_final)

        if filtro.hora_inicio:
            query = query.filter(ORMMensagem.hora >= filtro.hora_inicio)

        if filtro.hora_fim:
            query = query.filter(ORMMensagem.hora <= filtro.hora_fim)
        
        query = query.group_by(ORMMensagem.remetenteIp)
        resultados = query.all()
        
        dtos = [
            MensagemPorIpResponseDTO(
                ip=m.ip,
                quantidade_mensagens=m.quantidade_mensagens
            ) for m in resultados
        ]

        return dtos