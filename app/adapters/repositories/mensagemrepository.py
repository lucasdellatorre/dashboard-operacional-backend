from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, case, or_, and_
from app.application.dto.filtrodto import FiltroDTO
from app.domain.repositories.mensagemrepository import IMensagemRepository
from app.infraestructure.database.db import db
from app.domain.entities.mensagem import Mensagem as DomainMensagem
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem
from app.adapters.repositories.entities.ip import IP as ORMIp
from app.infraestructure.utils.logger import logger

class MensagemRepository(IMensagemRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_mensagens_from_numero_id(self, numero_id: int) -> list[DomainMensagem]:
        results = self.session.query(ORMMensagem).filter(ORMMensagem.numeroId == numero_id).all()
        if results is None:
            return []
        return [ORMMensagem.toMensagemEntidade(result) for result in results]

    def get_mensagens_by_ip(self, ip_id: int):
        from app.adapters.repositories.entities.ip import IP as ORMIP

        ip_obj = self.session.query(ORMIP).filter(ORMIP.id == ip_id).first()
        if not ip_obj:
            return []
        ip_str = ip_obj.ip
        mensagens = self.session.query(ORMMensagem).filter(ORMMensagem.remetenteIp == ip_str).all()

        return [ORMMensagem.toMensagemEntidade(m) for m in mensagens]

    def contar_mensagens_por_contato(
        self,
        numeros: list[str],
        tickets: list[str],
        grupo: str,
        tipo: str,
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
        
        if grupo and grupo.lower() != "all":
            grupo_lower = grupo.lower()
            if grupo_lower == "group":
                query = query.filter(ORMMensagem.grupoId.isnot(None))
            elif grupo_lower == "number":
                query = query.filter(ORMMensagem.grupoId.is_(None))
            else:
                logger.warning(f"Grupo '{grupo}' não reconhecido. Nenhum filtro aplicado.")

        if tipo and tipo.lower() != "all":
            query = query.filter(func.lower(ORMMensagem.tipoMensagem) == tipo.lower())

        if tickets:
            query = query.filter(ORMMensagem.internalTicketNumber.in_(tickets))

        if data_inicial:
            query = query.filter(ORMMensagem.data >= data_inicial)

        if data_final:
            query = query.filter(ORMMensagem.data <= data_final)

        if hora_inicio:
            query = query.filter(ORMMensagem.hora >= hora_inicio)

        if hora_fim:
            query = query.filter(ORMMensagem.hora <= hora_fim)

        query = query.group_by(contato_case).order_by(func.count(ORMMensagem.id).desc())

        resultados = query.all()

        return [{"contato": r.contato, "qtdMensagens": r.qtdMensagens} for r in resultados]

    def contar_mensagens_por_horario(
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

        # Extrai a hora como inteiro de 0 a 23
        hora_int = func.cast(func.substr(ORMMensagem.hora, 1, 2), db.Integer)

        # Define o índice da faixa
        faixa_index = case(
            (hora_int.between(0, 1), 0),
            (hora_int.between(2, 3), 1),
            (hora_int.between(4, 5), 2),
            (hora_int.between(6, 7), 3),
            (hora_int.between(8, 9), 4),
            (hora_int.between(10, 11), 5),
            (hora_int.between(12, 13), 6),
            (hora_int.between(14, 15), 7),
            (hora_int.between(16, 17), 8),
            (hora_int.between(18, 19), 9),
            (hora_int.between(20, 21), 10),
            (hora_int.between(22, 23), 11),
            else_=99
        ).label("idx")

        # Define o rótulo da faixa
        faixa_label = case(
            (hora_int.between(0, 1), "00:00-02:00"),
            (hora_int.between(2, 3), "02:00-04:00"),
            (hora_int.between(4, 5), "04:00-06:00"),
            (hora_int.between(6, 7), "06:00-08:00"),
            (hora_int.between(8, 9), "08:00-10:00"),
            (hora_int.between(10, 11), "10:00-12:00"),
            (hora_int.between(12, 13), "12:00-14:00"),
            (hora_int.between(14, 15), "14:00-16:00"),
            (hora_int.between(16, 17), "16:00-18:00"),
            (hora_int.between(18, 19), "18:00-20:00"),
            (hora_int.between(20, 21), "20:00-22:00"),
            (hora_int.between(22, 23), "22:00-00:00"),
            else_="Desconhecido"
        ).label("periodo")

        # Monta a query
        query = (
            self.session.query(
                faixa_index,
                faixa_label,
                func.count(ORMMensagem.id).label("qtdMensagens")
            )
            .filter(
                or_(
                    ORMMensagem.remetente.in_(numeros),
                    ORMMensagem.destinatario.in_(numeros)
                )
            )
        )

        # Filtros adicionais
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

        query = query.group_by(faixa_index, faixa_label).order_by(faixa_index)

        resultados = query.all()

        return [{"periodo": r.periodo, "qtdMensagens": r.qtdMensagens} for r in resultados]
          
    def contar_mensagens_por_dia(
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

        query = (
            self.session.query(
                func.date(ORMMensagem.data).label("data"),
                func.count(ORMMensagem.id).label("qtdMensagens")
            )
            .filter(
                or_(
                    ORMMensagem.remetente.in_(numeros),
                    ORMMensagem.destinatario.in_(numeros)
                )
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

        if tipo and tipo.lower() != "all":
            query = query.filter(func.lower(ORMMensagem.tipoMensagem) == tipo.lower())

        if data_inicial:
            query = query.filter(func.cast(ORMMensagem.data, db.Date) >= data_inicial)

        if data_final:
            query = query.filter(func.cast(ORMMensagem.data, db.Date) <= data_final)

        if hora_inicio:
            query = query.filter(ORMMensagem.hora >= hora_inicio)

        if hora_fim:
            query = query.filter(ORMMensagem.hora <= hora_fim)
            
        query = query.group_by(func.date(ORMMensagem.data)).order_by(func.date(ORMMensagem.data))

        resultados = query.all()

        return [{"data": r.data.strftime("%Y-%m-%d"), "qtdMensagens": r.qtdMensagens} for r in resultados]

    def contar_mensagens_por_ip(
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
        
        query = (
            self.session.query(
                ORMMensagem.remetenteIp.label("ip"),
                func.count(ORMMensagem.id).label("qtdMensagens")
            )
            .filter(ORMMensagem.remetente.in_(numeros))
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

        if tipo and tipo.lower() != "all":
            query = query.filter(func.lower(ORMMensagem.tipoMensagem) == tipo.lower())

        if data_inicial:
            query = query.filter(func.cast(ORMMensagem.data, db.Date) >= data_inicial)

        if data_final:
            query = query.filter(func.cast(ORMMensagem.data, db.Date) <= data_final)

        if hora_inicio:
            query = query.filter(ORMMensagem.hora >= hora_inicio)

        if hora_fim:
            query = query.filter(ORMMensagem.hora <= hora_fim)

        query = query.group_by(ORMMensagem.remetenteIp).order_by(func.count(ORMMensagem.id).desc())

        resultados = query.all()

        return [{"ip": r.ip, "qtdMensagens": r.qtdMensagens} for r in resultados]
      
    def buscar_por_filtro(
            self,
            numeros: Optional[List[str]],
            tickets: Optional[List[str]],
            tipo: Optional[str],
            grupo: Optional[str],
            data_inicial: Optional[str],
            data_final: Optional[str],
            hora_inicio: Optional[str],
            hora_fim: Optional[str]
    ) -> List[dict]:
        numeros_ids = []
        for numero in numeros or []:
            if len(numero) < 9:
                numeros_ids.append(numero)
                
        
        query = self.session.query(ORMMensagem).filter(or_(
                    ORMMensagem.numeroId.in_(numeros_ids),
                    ORMMensagem.remetente.in_(numeros)
                ))
        
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

        if tipo and tipo.lower() != "all":
            query = query.filter(func.lower(ORMMensagem.tipoMensagem) == tipo.lower())

        if data_inicial:
            query = query.filter(func.cast(ORMMensagem.data, db.Date) >= data_inicial)

        if data_final:
            query = query.filter(func.cast(ORMMensagem.data, db.Date) <= data_final)

        if hora_inicio:
            query = query.filter(ORMMensagem.hora >= hora_inicio)

        if hora_fim:
            query = query.filter(ORMMensagem.hora <= hora_fim)
    
        mensagens_orm = query.all()
      
        resultados = []
        for mensagem in mensagens_orm:
            resultados.append({
                "id": mensagem.id,
                "remetente": mensagem.remetente,
                "destinatario": mensagem.destinatario,
                "tipoMensagem": mensagem.tipoMensagem,
                "timestamp": mensagem.timestamp
            })

        return resultados
