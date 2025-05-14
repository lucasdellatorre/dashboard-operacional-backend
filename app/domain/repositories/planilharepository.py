from abc import ABC, abstractmethod
from app.domain.entities.planilha import Planilha

class IPlanilhaRepository(ABC):
    @abstractmethod
    def save(self, file_buffer, file_size, filename, operacao_id) -> None:
        raise (NotImplementedError)
    
    def get_all_ordered_by_upload_date(self):
        raise (NotImplementedError)        
