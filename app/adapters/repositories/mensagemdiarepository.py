from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from typing import List
from app.adapters.repositories.entities.interceptacao import Interceptacao
from app.adapters.repositories.entities.numero import Numero
from app.adapters.repositories.entities.numerosuspeito import NumeroSuspeito
from app.application.dto.mensagempordiaresponsedto import MensagemPorDiaResponseDTO
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem
from app.domain.repositories.mensagemdiarepository import IMensagemDiaRepository
from app.infraestructure.utils.logger import logger

class MensagemDiaRepository(IMensagemDiaRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def buscar_mensagens_por_dia(self, filtro: MensagensRequestDTO, ticket_numbers: List[str]) -> List[MensagemPorDiaResponseDTO]:

        numeros = list(filtro.numeros or [])
        
        query = (
            self.session
            .query(
                extract("dow", ORMMensagem.timestamp).label("dia_semana"),
                func.count(ORMMensagem.id).label("quantidade_mensagens"),
            )
            .filter(ORMMensagem.numeroId.in_(numeros))
        )
        
        if ticket_numbers:
            query = query.filter(ORMMensagem.internalTicketNumber.in_(ticket_numbers))
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

        if filtro.tipo and filtro.tipo.upper() != "all":
            query = query.filter(ORMMensagem.tipoMensagem == filtro.tipo)

        if filtro.data_inicial:
            query = query.filter(ORMMensagem.data >= filtro.data_inicial)

        if filtro.data_final:
            query = query.filter(ORMMensagem.data <= filtro.data_final)

        if filtro.hora_inicio:
            query = query.filter(ORMMensagem.hora >= filtro.hora_inicio)

        if filtro.hora_fim:
            query = query.filter(ORMMensagem.hora <= filtro.hora_fim)

        query = query.group_by(extract("dow", ORMMensagem.timestamp))
        result = query.all()
        
        dtos = [
            MensagemPorDiaResponseDTO(
                dia_semana=row.dia_semana,
                quantidade_mensagens=row.quantidade_mensagens
            )
            for row in result
        ]
        
        return dtos
