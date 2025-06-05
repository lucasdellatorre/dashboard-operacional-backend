class SuspeitoEmail():
    def __init__(self, suspeitoId, email, lastUpdateCpf, lastUpdateDate = None, id=None):
        self.id = id
        self.suspeitoId = suspeitoId
        self.email = email
        self.lastUpdateCpf = lastUpdateCpf
        self.lastUpdateDate = lastUpdateDate
        
    def to_dict(self):
        return {
            "id": self.id,
            "suspeitoId": self.suspeitoId,
            "email": self.email,
            "lastUpdateCpf": self.lastUpdateCpf,
            "lastUpdateDate": self.lastUpdateDate,
        }
        