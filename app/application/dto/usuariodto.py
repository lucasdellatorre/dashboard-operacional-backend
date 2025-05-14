from app.domain.entities.usuario import Usuario

class UsuarioDTO:
    def __init__(self, cpf, id: int | None = None):
        self.id = id
        self.cpf = cpf
        
    def to_dict(self):
        return {
            'id': self.id,
            'cpf': self.cpf
        }
        
    @staticmethod
    def fromEntity(usuario: Usuario):
        return UsuarioDTO(id=usuario.id, cpf=usuario.cpf)