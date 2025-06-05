from sqlalchemy.orm import Session
from app.domain.repositories.iprepository import IIPRepository
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.ip import IP as ORMIP

class IPRepository(IIPRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_all_ordered_by_last_access(self):
        return self.session.query(ORMIP).order_by(ORMIP.timestamp.asc()).all()