from app.adapters.repositories.planilharepository import PlanilhaRepository
from app.application.usecases.getallplanilhausecase import GetAllPlanilhaUseCase
from app.domain.services.planilhaservice import PlanilhaService

class PlanilhaFactory:
    @staticmethod
    def get_all_Planilha():
        planilha_repository = PlanilhaRepository()
        planilha_service = PlanilhaService(planilha_repository)
        return GetAllPlanilhaUseCase(planilha_service)
