from typing import List
from app.application.dto.planilhadto import PlanilhaDTO
from app.domain.services.planilhaservice import PlanilhaService 

class GetAllPlanilhaUseCase:
    def __init__(self, planilha_service: PlanilhaService):
        self.planilha_service = planilha_service

    def execute(self) -> List[PlanilhaDTO]:
        planilhas = self.planilha_service.list_planilhas()
        return [PlanilhaDTO.fromEntity(planilha) for planilha in planilhas]
    