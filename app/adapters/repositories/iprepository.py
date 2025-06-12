from sqlalchemy import func
from sqlalchemy.orm import Session
from app.domain.repositories.iprepository import IIPRepository
from app.infraestructure.database.db import db
from app.adapters.repositories.entities.ip import IP as ORMIP

class IPRepository(IIPRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def get_all_ordered_by_last_access(self):
        # Query grouped IPs and count
        results = (
            self.session.query(ORMIP.ip, func.count().label("ocorrencias"))
            .group_by(ORMIP.ip)
            .order_by(func.max(ORMIP.timestamp).desc())
            .all()
        )

        return [{"ip": row.ip, "ocorrencias": row.ocorrencias} for row in results]
    

    def find(self, ip: list):
        return self.session.query(ORMIP).filter(ORMIP.ip == ip).all()