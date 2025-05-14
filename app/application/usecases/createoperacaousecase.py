from app.application.dto.operacaodto import OperacaoDTO
from app.domain.services.operacaoservice import OperacaoService

class CreateOperacaoUseCase:
    def __init__(self, operacao_service: OperacaoService):
        self.operacao_service = operacao_service

    def execute(self, operacao_dto: OperacaoDTO) -> OperacaoDTO:
        nome = operacao_dto.nome

        if self.operacao_service.find_by_name(nome):
            raise ValueError('operation already exists!')
        
        new_operation = self.operacao_service.create_operacao(nome)
        return OperacaoDTO.fromEntity(new_operation)
    
    
    
    