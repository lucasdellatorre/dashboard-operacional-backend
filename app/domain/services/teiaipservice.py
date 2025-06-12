class TeiaIPService:
    def __init__(self, ip_repository):
        self.repository = ip_repository

    def find(self, id: int):
        results = self.repository.find([id])
        return results[0] if results else None