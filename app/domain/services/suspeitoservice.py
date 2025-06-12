from datetime import datetime
from typing import Optional, List

from app.application.dto.mensagensrequestdto import MensagensRequestDTO
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
    
    def get_info_e_numeros_by_id(self, id: int) -> dict | None:
        suspeito: SuspeitoEntity = self.suspeito_repository.get_by_id(id)
        if not suspeito:
            return None
        numeros: list[int] = self.suspeito_repository.get_numeros_by_suspeito_ids([id])
        return {
            "id": suspeito.id,
            "nome": suspeito.nome,
            "cpf": suspeito.cpf,
            "apelido": suspeito.apelido,
            "anotacoes": suspeito.anotacoes,
            "relevante": suspeito.relevante,
            "numeros": numeros
        }


    def get_numeros_by_suspeito_ids(self, suspeito_ids: list[int]) -> list[dict]:
        numeros = self.suspeito_repository.get_numeros_by_suspeito_ids(suspeito_ids)
        return [{"numero": numero} for numero in numeros]
            
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
    
    def add_telefone(self, suspeito_id, numeros, cpf):
        return self.suspeito_repository.add_telefone(suspeito_id, numeros, cpf)

    def get_all_email(self, suspeito_id):
        return self.suspeito_repository.get_all_email(suspeito_id)
            
    def atualizar_suspeito(self, id, dados: dict):
        suspeito = self.suspeito_repository.get_by_id(id)
        if not suspeito:
            raise LookupError(f"Suspeito com ID {id} não encontrado.")

        # Validação do CPF se fornecido
        if "cpf" in dados:
            cpf = dados["cpf"]
            if cpf is not None:
                if not isinstance(cpf, str) or not cpf.isdigit() or len(cpf) != 11:
                    raise ValueError("CPF inválido. Deve conter exatamente 11 dígitos numéricos.")
                suspeito.cpf = cpf

        # Atualiza campos simples se presentes
        for campo in ["nome", "apelido", "anotacoes", "relevante"]:
            if campo in dados:
                setattr(suspeito, campo, dados[campo])

        # Campos de auditoria
        suspeito.lastUpdateDate = datetime.utcnow()
        suspeito.lastUpdateCpf = dados.get("lastUpdateCpf")

        # Salva no repositório
        return self.suspeito_repository.atualizar(suspeito)
    
    def _check_numeros_em_uso(self, numero_ids: list[int]):
        for numero_id in numero_ids:
            suspeito = self.suspeito_repository.get_by_numero_id_with_relations(numero_id)
            if suspeito:
                raise ValueError(f"O número {numero_id} já está vinculado ao suspeito '{suspeito.apelido}'.")

    def is_suspeito(self, suspeito_id):
        return self.suspeito_repository.is_suspeito(suspeito_id)

    def deletar(self, id: int):
        suspeito = self.suspeito_repository.get_by_id(id)
        if not suspeito:
            raise LookupError(f"Suspeito com ID {id} não encontrado.")

        self.suspeito_repository.deletar(id)

    def update_email(self, dto):
        email = self.suspeito_repository.get_email_by_id(dto.email_id)
        if not email:
            raise LookupError(f"E-mail com ID {dto.email_id} não encontrado.")

        email.email = dto.email
        email.lastUpdateCpf = dto.last_update_cpf
        email.lastUpdateDate = datetime.utcnow()

        return self.suspeito_repository.update_email(email)

    def buscar_por_filtro(self, filtro_dto: MensagensRequestDTO) -> List[SuspeitoEntity]:
        return self.suspeito_repository.buscar_por_filtro(
            numeros=filtro_dto.numeros,
            suspeitos=filtro_dto.suspeitos,
            operacoes=filtro_dto.operacoes,
            grupo=filtro_dto.grupo,
            tipo=filtro_dto.tipo,
            data_inicial=filtro_dto.data_inicial,
            data_final=filtro_dto.data_final,
            hora_inicio=filtro_dto.hora_inicio,
            hora_fim=filtro_dto.hora_fim
        )