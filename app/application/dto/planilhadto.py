from app.domain.entities.planilha import Planilha

class PlanilhaDTO:
    def __init__(self, nome, data_upload, size, id: int  | None = None):
        self.id = id
        self.nome = nome
        self.data_upload = data_upload
        self.size = size
        # self.user_id = user_id
        
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_upload': self.data_upload.isoformat() if self.data_upload else None,
            'size': self.size,
        #    'user_id': self.user_id
        }
        
    @staticmethod
    def fromEntity(planilha: Planilha):
        return PlanilhaDTO(id=planilha.id, nome=planilha.nome, data_upload=planilha.dataUpload, size=planilha.size)