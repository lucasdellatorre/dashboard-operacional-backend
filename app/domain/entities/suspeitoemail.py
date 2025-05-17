class SuspeitoEmail():
    def __init__(self, suspeitoId, email, lastUpdateCpf, lastUpdateDate, id=None):
        self.id = id
        self.suspeitoId = suspeitoId
        self.email = email
        self.lastUpdateCpf = lastUpdateCpf
        self.lastUpdateDate = lastUpdateDate
        