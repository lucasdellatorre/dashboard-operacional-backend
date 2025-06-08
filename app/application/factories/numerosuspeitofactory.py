from app.domain.services.numerosuspeitoservice import NumeroSuspeitoService
from app.adapters.repositories.numerosuspeitorepository import NumeroSuspeitoRepository
from app.application.usecases.deletenumerosuspeitousecase import DeleteNumeroSuspeitoUseCase

class NumeroSuspeitoFactory:
    @staticmethod
    def delete_number():
        numero_suspeito_repo = NumeroSuspeitoRepository()
        numero_suspeito_service = NumeroSuspeitoService(numero_suspeito_repo)
        return DeleteNumeroSuspeitoUseCase(numero_suspeito_service)
