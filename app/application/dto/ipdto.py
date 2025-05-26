from app.domain.entities.ip import IP

class IPDTO:
    def __init__(self, id: int, internalTicketNumber: str, ip: str, versao: str, numeroId: int):
        self.id = id
        self.internalTicketNumber = internalTicketNumber
        self.ip = ip
        self.versao = versao
        self.numeroId = numeroId
        
    def to_dict(self):
        return {
            'id': self.id,
            'internalTicketNumber': self.internalTicketNumber,
            'ip': self.ip,
            'versao': self.versao,
            'numeroId': self.numeroId
        }
        
    @staticmethod
    def fromEntity(ip: IP):
        return IPDTO(id = ip.id, internalTicketNumber = ip.internalTicketNumber, ip = ip.ip, versao = ip.versao, numeroId = ip.numeroId)
    
