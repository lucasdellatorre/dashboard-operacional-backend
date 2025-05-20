from datetime import datetime
from app.domain.repositories.suspeitorepository import ISuspeitoRepository
from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.suspeito import Suspeito as SuspeitoEntity
from app.application.dto.createsuspeitodto import CreateSuspeitoDTO
from app.domain.entities.numerosuspeito import NumeroSuspeito as NumeroSuspeitoEntity
from app.domain.entities.suspeitoemail import SuspeitoEmail as SuspeitoEmailEntity

class SuspeitoService:
    def __init__(
        self,
        suspeito_repository: ISuspeitoRepository,
        numero_repository: INumeroRepository
    ):
        self.suspeito_repository = suspeito_repository
        self.numero_repository = numero_repository

    def get_by_id(self, id: int) -> SuspeitoEntity | None:
        return self.suspeito_repository.get_by_id_with_relations(id)

    def get_suspeito_by_numero_id(self, numero_id: int) -> dict | None:
        suspeito = self.suspeito_repository.get_by_numero_id_with_relations(numero_id)
        if not suspeito:
            return None
        return {
            "apelido": suspeito.apelido,
            "numeros": [num.numero for num in suspeito.numeros]
        }

    def find_by_name(self, apelido: str) -> SuspeitoEntity | None:
        return self.suspeito_repository.get_by_apelido(apelido)

    def create_suspeito(self, dto: CreateSuspeitoDTO) -> SuspeitoEntity:
        self._check_numeros_em_uso(dto.numeros_ids)

        numeros = self.numero_repository.get_all_by_ids(dto.numeros_ids)
        if not numeros or len(numeros) != len(dto.numeros_ids):
            raise ValueError("Um ou mais números fornecidos são inválidos.")

        numero_suspeito_entities = [
            NumeroSuspeitoEntity(
                numero=n,
                lastUpdateDate=datetime.utcnow().isoformat(),
                lastUpdateCpf=dto.lastUpdateCpf or "00000000000"
            )
            for n in numeros
        ]

        suspeito = SuspeitoEntity(
            nome=dto.nome,
            cpf=dto.cpf,
            anotacoes="",
            apelido=dto.apelido,
            relevante=False,
            emails=[],
            numerosuspeito=numero_suspeito_entities
        )

        return self.suspeito_repository.create(suspeito)
    
    def create_email(self, suspeito_email: SuspeitoEmailEntity):
        return self.suspeito_repository.create_email(suspeito_email)
    
    def delete_email(self, suspeito_id, email_id):
        return self.suspeito_repository.delete_email(suspeito_id, email_id)
    
    def _check_numeros_em_uso(self, numero_ids: list[int]):
        for numero_id in numero_ids:
            suspeito = self.suspeito_repository.get_by_numero_id_with_relations(numero_id)
            if suspeito:
                raise ValueError(f"O número {numero_id} já está vinculado ao suspeito '{suspeito.apelido}'.")
        