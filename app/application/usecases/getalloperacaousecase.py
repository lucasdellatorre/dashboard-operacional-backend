from app.application.dto.operacaocomalvosdto import OperacaoComAlvosDTO
from app.application.dto.operacaodto import OperacaoDTO
from app.domain.services.operacaoservice import OperacaoService

class GetAllOperacaoUseCase:
    def __init__(self, operacao_service: OperacaoService):
        self.operacao_service = operacao_service

    def execute(self) -> list[OperacaoComAlvosDTO]:
        operacoes = self.operacao_service.get_all_operacoes()
        return operacoes