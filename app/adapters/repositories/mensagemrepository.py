from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.domain.repositories.operacaorepository import IOperacaoRepository
from app.domain.entities.mensagem import Mensagem as DomainMensagem
from app.adapters.repositories.entities.mensagens import Mensagem as ORMMensagem

class MensagemRepository():
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_mensagens_from_numero_id(self, numero_id) -> list[DomainMensagem]:
        results = self.session.query(ORMMensagem).filter(ORMMensagem.numeroId == numero_id).all()
        if results is None: return []
        return [ORMMensagem.toMensagemEntidade(result) for result in results]

    def get_mensagens_by_ip(self, ip_id: int):
        from app.adapters.repositories.entities.ip import IP as ORMIP

        ip_obj = self.session.query(ORMIP).filter(ORMIP.id == ip_id).first()
        if not ip_obj:
            return []
        ip_str = ip_obj.ip
        mensagens = self.session.query(ORMMensagem).filter(ORMMensagem.remetenteIp == ip_str).all()

        return [ORMMensagem.toMensagemEntidade(m) for m in mensagens]