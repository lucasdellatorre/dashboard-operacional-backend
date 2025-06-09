from datetime import datetime
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import SQLAlchemyError
from app.domain.repositories.suspeitorepository import ISuspeitoRepository
from app.domain.entities.suspeito import Suspeito as SuspeitoEntity
from app.domain.entities.numerosuspeito import NumeroSuspeito as NumeroSuspeitoEntity
from app.domain.entities.numero import Numero as NumeroEntity
from app.domain.entities.suspeitoemail import SuspeitoEmail as SuspeitoEmailEntity
from app.domain.entities.ip import IP as IPEntity
from app.adapters.repositories.entities.suspeito import Suspeito as ORMSuspeito
from app.adapters.repositories.entities.numero import Numero as ORMSNumero
from app.adapters.repositories.entities.numerosuspeito import NumeroSuspeito as ORMNumeroSuspeito
from app.adapters.repositories.entities.suspeitoemail import SuspeitoEmail as ORMSuspeitoEmail
from app.adapters.repositories.entities.numero import Numero as ORMNumero
from app.infraestructure.database.db import db
from app.infraestructure.utils.logger import logger

class SuspeitoRepository(ISuspeitoRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def atualizar(self, id: int, dados: dict):
        suspeito = self.session.query(ORMSuspeito).get(id)
        if not suspeito:
            raise LookupError("Suspeito não encontrado.")
        
        suspeito.lastUpdateDate = datetime.now()
        suspeito.lastUpdateCpf = dados['lastUpdateCpf']

        for campo in ['nome', 'cpf', 'apelido', 'anotacoes', 'relevante']:
            if campo in dados:
                setattr(suspeito, campo, dados[campo])

        self.session.commit()
        return ORMSuspeito.toEntity(suspeito)

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
                    ips=[]
                ),
                lastUpdateCpf=None,
                lastUpdateDate=None
            )
            for ns in suspeito.numero_suspeitos
        ]

        return SuspeitoEntity(
            id=suspeito.id,
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
    
    def get_by_apelido(self, apelido: str) -> SuspeitoEntity | None:
        orm_obj = (
            db.session.query(ORMSuspeito)
            .filter(ORMSuspeito.apelido == apelido)
            .first()
        )

        if not orm_obj:
            return None

        return SuspeitoEntity(
            id=orm_obj.id,
            nome=orm_obj.nome,
            apelido=orm_obj.apelido,
            cpf=orm_obj.cpf,
            relevante=orm_obj.relevante,
            anotacoes=orm_obj.anotacoes,
            lastUpdateDate=orm_obj.lastUpdateDate,
            lastUpdateCpf=orm_obj.lastUpdateCpf,
            emails=[],  
            numerosuspeito=[]
        )    
    
    def create(self, suspeito: SuspeitoEntity) -> SuspeitoEntity:
        try:
            orm_obj = ORMSuspeito(
                apelido=suspeito.apelido,
                nome=suspeito.nome,
                cpf=suspeito.cpf,
                anotacoes=suspeito.anotacoes,
                relevante=suspeito.relevante,
                lastUpdateDate=suspeito.lastUpdateDate or datetime.utcnow(),
                lastUpdateCpf=suspeito.lastUpdateCpf
            )

            db.session.add(orm_obj)
            db.session.flush()

            for ns in suspeito.numerosuspeito:
                db.session.add(
                    ORMNumeroSuspeito(
                        suspeitoId=orm_obj.id,
                        numeroId=ns.numero.id,
                        lastUpdateDate=ns.lastUpdateDate or datetime.utcnow(),
                        lastUpdateCpf=ns.lastUpdateCpf
                    )
                )
                
            for email in suspeito.emails:
                db.session.add(
                    ORMSuspeitoEmail(
                        suspeitoId=orm_obj.id,
                        email=email.email,
                        lastUpdateDate=email.lastUpdateDate or datetime.utcnow(),
                        lastUpdateCpf=email.lastUpdateCpf
                    )
                )

            db.session.commit()

            # retorna a entidade com ID preenchido
            return SuspeitoEntity(
                id=orm_obj.id,
                nome=orm_obj.nome,
                apelido=orm_obj.apelido,
                cpf=orm_obj.cpf,
                relevante=orm_obj.relevante,
                anotacoes=orm_obj.anotacoes,
                lastUpdateDate=orm_obj.lastUpdateDate,
                lastUpdateCpf=orm_obj.lastUpdateCpf,
                emails=suspeito.emails,
                numerosuspeito=suspeito.numerosuspeito
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def create_email(self, suspeito_email: SuspeitoEmailEntity) -> bool:
        try:
            email_orm = ORMSuspeitoEmail.fromSuspeitoEmailEntidade(suspeito_email)
            db.session.add(email_orm)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return False
        
    def delete_email(self, suspeito_id, email_id) -> bool:
        try:
            db.session.query(ORMSuspeitoEmail).filter(ORMSuspeitoEmail.id == email_id, ORMSuspeitoEmail.suspeitoId == suspeito_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return False
        
    def get_all_email(self, suspeito_id):
        results = db.session.query(ORMSuspeitoEmail).filter(ORMSuspeitoEmail.suspeitoId == suspeito_id).all()
        return [ORMSuspeitoEmail.toSuspeitoEmailEntidade(result) for result in results]
    
    def is_suspeito(self, suspeito_id):
        result = db.session.query(ORMSuspeito).filter(ORMSuspeito.id == suspeito_id)
        if result: 
            return True
        else:
            return False
        
    def add_telefone(self, suspeito_id, telefoneId, cpf) -> bool:
        suspeito: ORMSuspeito = self.session.query(ORMSuspeito).get(suspeito_id)
        if not suspeito:
            return False                   

        numero_orm: ORMNumero = self.session.query(ORMNumero).get(telefoneId)
        
        if not numero_orm:
            return False

        exists = self.session.query(ORMNumeroSuspeito).filter_by(
            suspeitoId=suspeito.id,
            numeroId=numero_orm.id
        ).first()
        if exists:
            return True 

        self.session.add(
            ORMNumeroSuspeito(
                suspeitoId=suspeito.id,
                numeroId=numero_orm.id,
                lastUpdateDate=datetime.now(),
                lastUpdateCpf=cpf
            )
        )
        
        self.session.commit()

        return True