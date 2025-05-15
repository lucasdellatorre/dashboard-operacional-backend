from app.domain.services.numeroservice import NumeroService
from app.application.dto.listaoperacaodto import ListaOperacaoDTO

class ListarOperacoesUseCase:
    def __init__(self, numero_service: NumeroService):
        self.numero_service = numero_service

    def execute(self, operacao_ids: list[int]):
        rows = self.numero_service.listar_por_operacoes(operacao_ids)
        return [ListaOperacaoDTO.from_dict(row) for row in rows]
