from app.domain.services.suspeitoservice import SuspeitoService

class DeletarSuspeitoUseCase:
    def __init__(self, service: SuspeitoService):
        self.service = service

    def execute(self, id: int):
        """
        Executa a remoção de um suspeito pelo ID.
        Lança LookupError se o suspeito não existir.
        """
        self.service.deletar(id)