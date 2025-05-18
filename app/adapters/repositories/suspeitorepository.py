from sqlalchemy.orm import joinedload
from app.domain.repositories.suspeitorepository import ISuspeitoRepository
from app.domain.entities.suspeito import Suspeito as SuspeitoEntity
from app.domain.entities.numerosuspeito import NumeroSuspeito as NumeroSuspeitoEntity
from app.domain.entities.numero import Numero as NumeroEntity
from app.domain.entities.suspeitoemail import SuspeitoEmail as SuspeitoEmailEntity
from app.domain.entities.ip import IP as IPEntity
from app.adapters.repositories.entities.suspeito import Suspeito as ORMSuspeito
from app.adapters.repositories.entities.numero import Numero as ORMSNumero
from app.adapters.repositories.entities.numerosuspeito import NumeroSuspeito as ORMNumeroSuspeito
from app.infraestructure.database.db import db

class SuspeitoRepository(ISuspeitoRepository):
    def get_by_id_with_relations(self, id: int) -> SuspeitoEntity | None:
        orm_obj = (
            db.session.query(ORMSuspeito)
            .options(
                joinedload(ORMSuspeito.emails),
                joinedload(ORMSuspeito.numero_suspeitos)
                .joinedload(ORMNumeroSuspeito.numero)
                .joinedload(ORMSNumero.ips)
            )
            .filter(ORMSuspeito.id == id)
            .first()
        )

        if not orm_obj:
            return None

        numeros = [
            NumeroSuspeitoEntity(
                numero=NumeroEntity(
                    id=ns.numero.id,
                    numero=ns.numero.numero,
                    internalTicketNumber=ns.numero.internalTicketNumber,
                    ips=[
                        IPEntity(
                            id=ip.id,
                            ip=ip.ip,
                            versao=ip.versao,
                            data=ip.data,
                            hora=ip.hora,
                            timestamp=ip.timestamp,
                            numeroId=ip.numeroId,
                            internalTicketNumber=ip.internalTicketNumber
                        )
                        for ip in ns.numero.ips
                    ]
                ),
                lastUpdateCpf=ns.lastUpdateCpf,
                lastUpdateDate=ns.lastUpdateDate
            )
            for ns in orm_obj.numero_suspeitos
        ]

        emails = [
            SuspeitoEmailEntity(
                id=email.id,
                email=email.email,
                lastUpdateCpf=email.lastUpdateCpf,
                lastUpdateDate=email.lastUpdateDate,
                suspeitoId=email.suspeitoId
            )
            for email in orm_obj.emails
        ]

        return SuspeitoEntity(
            id=orm_obj.id,
            internalTicketNumber=orm_obj.internalTicketNumber,
            nome=orm_obj.nome,
            apelido=orm_obj.apelido,
            cpf=orm_obj.cpf,
            relevante=orm_obj.relevante,
            anotacoes=orm_obj.anotacoes,
            lastUpdateDate=orm_obj.lastUpdateDate,
            lastUpdateCpf=orm_obj.lastUpdateCpf,
            emails=emails,
            numerosuspeito=numeros
        )
    
    def get_by_numero_id_with_relations(self, numero_id: int) -> SuspeitoEntity | None:
        numero_suspeito = (
            db.session.query(ORMNumeroSuspeito)
            .filter(ORMNumeroSuspeito.numeroId == numero_id)
            .first()
        )

        if not numero_suspeito:
            return None

        suspeito = (
            db.session.query(ORMSuspeito)
            .options(
                joinedload(ORMSuspeito.numero_suspeitos)
                .joinedload(ORMNumeroSuspeito.numero)
            )
            .filter(ORMSuspeito.id == numero_suspeito.suspeitoId)
            .first()
        )

        if not suspeito:
            return None

        numeros = [
            NumeroSuspeitoEntity(
                numero=NumeroEntity(
                    id=ns.numero.id,
                    numero=ns.numero.numero,
                    internalTicketNumber=None,
                    ips=[]
                ),
                lastUpdateCpf=None,
                lastUpdateDate=None
            )
            for ns in suspeito.numero_suspeitos
        ]

        return SuspeitoEntity(
            id=suspeito.id,
            internalTicketNumber=None,
            nome=None,
            apelido=suspeito.apelido,
            cpf=None,
            relevante=None,
            anotacoes=None,
            lastUpdateDate=None,
            lastUpdateCpf=None,
            emails=[],
            numerosuspeito=numeros
        )
