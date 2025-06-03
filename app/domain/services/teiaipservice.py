class TeiaIPService:
    def __init__(self, ip_repository):
        self.repository = ip_repository

    def find(self, ip_id):
        return self.repository.find(ip_id)