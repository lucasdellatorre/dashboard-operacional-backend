from sqlalchemy.orm import Session
from app.infraestructure.database.db import db
from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.numero import Numero as DomainNumero
from app.adapters.repositories.entities.numero import Numero as ORMNumero
from app.adapters.repositories.entities.interceptacaonumero import InterceptacaoNumero as ORMInterceptacaoNumero

class NumeroRepository(INumeroRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def find(self, numero_id) -> DomainNumero:
        result = self.session.query(ORMNumero).get(int(numero_id))
        return ORMNumero.toNumeroEntidade(result)
    
    def isAlvo(self, numero_id) -> bool:
        result = self.session.query(ORMInterceptacaoNumero).filter(ORMInterceptacaoNumero.numeroId == int(numero_id), ORMInterceptacaoNumero.isAlvo == True).first()
        return result is not None