from typing import List
from app.application.dto.ipdto import IPDTO
from app.domain.services.ipservice import IPService 

class GetAllIPUseCase:
    def __init__(self, ip_service: IPService):
        self.ip_service = ip_service

    def execute(self) -> List[IPDTO]:
        ips = self.ip_service.list_ips()
        ips_sorted = sorted(ips, key=lambda ip: ip.timestamp, reverse=True)
        return [IPDTO.fromEntity(ip) for ip in ips_sorted]
    