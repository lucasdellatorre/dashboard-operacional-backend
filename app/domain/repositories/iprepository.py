from abc import ABC
from app.domain.entities.ip import IP

class IIPRepository(ABC):
    def get_all_ordered_by_last_access(self):
        raise (NotImplementedError)        
