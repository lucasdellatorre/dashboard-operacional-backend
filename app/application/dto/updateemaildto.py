class UpdateEmailDTO:
    def __init__(self, email_id: int, email: str, cpf_usuario: str):
        self.email_id = email_id
        self.email = email
        self.last_update_cpf = cpf_usuario

    @staticmethod
    def from_dict(data: dict, email_id: int, cpf_usuario: str):
        email = data.get("email")
        if not email:
            raise ValueError("O campo 'email' é obrigatório.")
        
        return UpdateEmailDTO(
            email_id=email_id,
            email=email,
            cpf_usuario=cpf_usuario
        )
