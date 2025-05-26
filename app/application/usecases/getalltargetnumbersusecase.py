from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService
from app.domain.services.suspeitoservice import SuspeitoService
from app.application.dto.numerosimplesdto import NumeroSimplesDTO

class GetAllTargetNumbersUseCase:
    def __init__(
        self,
        interceptacao_numero_service: InterceptacaoNumeroService,
        suspeito_service: SuspeitoService
    ):
        self.interceptacao_numero_service = interceptacao_numero_service
        self.suspeito_service = suspeito_service

    def execute(self, show_suspects: bool) -> list[NumeroSimplesDTO]:
        if show_suspects:
            data = self.interceptacao_numero_service.listar_numeros_com_suspeito_e_numeros()
            return [
                NumeroSimplesDTO(
                    id=row["id"],
                    value=row["value"],
                    suspect=row["suspect"],
                    numeros=row["numeros"]
                )
                for row in data
            ]

        numeros_interceptados = self.interceptacao_numero_service.get_all_numeros()
        return [
            NumeroSimplesDTO(
                id=row["id"],
                value=row["numero"],
                suspect=False,
                numeros=[]
            )
            for row in numeros_interceptados
        ]
        