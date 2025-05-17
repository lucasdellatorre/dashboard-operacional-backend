from datetime import datetime
from app.application.dto.operacaocomalvosdto import OperacaoComAlvosDTO
from app.domain.repositories.operacaorepository import IOperacaoRepository
from app.domain.entities.operacao import Operacao

class OperacaoService():
    def __init__(self, operacao_repository: IOperacaoRepository):
        self.operacao_repository = operacao_repository
        
    def hasOperacao(self, operacao_id) -> bool:
        return self.operacao_repository.hasOperacao(operacao_id)

    def get_all_operacoes(self):
        results = self.operacao_repository.get_all_operations()
        operacoes = []
        
        for orm_operacao, total_numeros_interceptados in results:
            operacao_entity = Operacao(
                id=orm_operacao.id,
                nome=orm_operacao.nome,
                dataCriacao=orm_operacao.dataCriacao
            )
            dto = OperacaoComAlvosDTO.fromEntity(
                operacao=operacao_entity,
                qtd_alvos=total_numeros_interceptados
            )
            operacoes.append(dto)
        
        return operacoes
    
    def create_operacao(self, nome: str) -> Operacao:
        operacao = Operacao(nome=nome, dataCriacao= datetime.now())
        return self.operacao_repository.create(operacao)
    
    def find_by_name(self, nome: str) -> bool:
        return self.operacao_repository.find_by_name(nome)
    
    
        
    

    
    
    
