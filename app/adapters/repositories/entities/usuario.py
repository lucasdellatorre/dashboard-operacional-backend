from sqlalchemy import Column
from sqlalchemy.types import Integer, CHAR
from app.infraestructure.database.db import db
from app.domain.entities.usuario import Usuario as UsuarioEntidade

class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement="auto")
    cpf = Column(CHAR(11), unique=True, nullable=False)
    
    def __repr__(self):
        return f"User(id={self.id}, cpf={self.cpf})"
    
    @staticmethod
    def fromUsuarioEntidade(usuario: UsuarioEntidade) -> "Usuario":
        """Converts a domain entity to an ORM model instance."""
        return Usuario(id=usuario.id, cpf=usuario.cpf)
    
    @staticmethod
    def toUsuarioEntidade(usuario: "Usuario") -> UsuarioEntidade:
        """Converts an ORM model instance to a domain entity."""
        return UsuarioEntidade(id=usuario.id, cpf=usuario.cpf)