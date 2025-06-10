from dataclasses import dataclass

@dataclass
class CreateEmailDTO:
    cpf: str
    email: str
    suspeitoId: int

    @staticmethod
    def from_dict(data: dict, id: int, cpf: str):
        email = data.get("email")

        if not id:
            raise ValueError("O campo 'id' é obrigatório.")
        if not cpf:
            raise ValueError("O campo 'cpf' é obrigatório.")
        if not email:
            raise ValueError("O campo 'email' é obrigatório.")
   
        return CreateEmailDTO(
            cpf=cpf,
            email=email,
            suspeitoId=id
        )