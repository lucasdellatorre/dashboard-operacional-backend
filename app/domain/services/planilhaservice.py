from app.domain.repositories.planilharepository import IPlanilhaRepository

class PlanilhaService:
    def __init__(self, planilha_repository: IPlanilhaRepository):
        self.planilha_repository = planilha_repository

    def list_planilhas(self):
        return self.planilha_repository.get_all_ordered_by_upload_date()