from app.domain.repositories.suspeitorepository import ISuspeitoRepositoryInterface

class SuspeitoService:
    def __init__(self, suspeito_repository: ISuspeitoRepositoryInterface):
        self.repo = suspeito_repository  

    def atualizar_suspeito(self, id, dados):
        cpf = dados.get("cpf")
        if cpf is not None and (not cpf.isdigit() or len(cpf) != 11):
            raise ValueError("CPF inválido. Deve conter exatamente 11 dígitos numéricos.")
        
        return self.repo.atualizar(id, dados)
