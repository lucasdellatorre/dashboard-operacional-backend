from app.domain.repositories.iprepository import IIPRepository

class IPService:
    def __init__(self, ip_repository: IIPRepository):
        self.ip_repository = ip_repository

    def list_ips(self):
        return self.ip_repository.get_all_ordered_by_last_access()