from typing import List
from app.application.dto.ipdto import IPDTO
from app.domain.services.ipservice import IPService 

class GetAllIPUseCase:
    def __init__(self, ip_service: IPService):
        self.ip_service = ip_service

    def execute(self) -> List[IPDTO]:
        return self.ip_service.list_ips()