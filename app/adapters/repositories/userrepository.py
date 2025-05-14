from sqlalchemy.orm import Session
from app.domain.repositories.usuariorepository import IUsuarioRepository
from app.infraestructure.database.db import db
from app.domain.entities.usuario import Usuario as DomainUsuario
from app.adapters.repositories.entities.usuario import Usuario as ORMUsuario

class UserRepository(IUsuarioRepository):
    def __init__(self, session: Session = db.session):
        self.session = session
        
    def create(self, usuario: DomainUsuario) -> DomainUsuario:
        orm_usuario = ORMUsuario.fromUsuarioEntidade(usuario)
        self.session.add(orm_usuario)
        self.session.commit()
        return ORMUsuario.toUsuarioEntidade(orm_usuario)