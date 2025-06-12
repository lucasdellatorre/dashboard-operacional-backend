from abc import ABC, abstractmethod
from app.domain.entities.ip import IP

class IIPRepository(ABC):
    @abstractmethod
    def get_all_ordered_by_last_access(self):
        raise (NotImplementedError)        
