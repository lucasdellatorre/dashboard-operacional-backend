from flask import request, Blueprint
from flask_restful import Api, Resource
from app.application.factories.suspeitofactory import SuspeitoFactory
from app.application.dto.createsuspeitodto import CreateSuspeitoDTO
from app.application.dto.createemaildto import CreateEmailDTO
from app.application.usecases.createemailusecase import CreateEmailUseCase


# --- POST controller ---
class SuspeitoCreateController(Resource):
    def __init__(self, **kwargs):
        self.create_suspeito_use_case = kwargs['create_suspeito_use_case']

    def post(self):
        """
        Cria um novo suspeito.
        ---
        tags:
          - Suspeito
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - apelido
                - numeros_ids
              properties:
                apelido:
                  type: string
                nome:
                  type: string
                cpf:
                  type: string
                numeros_ids:
                  type: array
                  items:
                    type: integer
          - name: cpfUsuario
            in: header
            required: true
            schema:
              type: string
              example: "12345678900"
        responses:
          201:
            description: Suspeito criado com sucesso
          400:
            description: Erro de validação
          500:
            description: Erro interno
        """
        data = request.get_json()
        cpf_usuario = request.headers.get("cpfUsuario")

        if not cpf_usuario:
            return {"message": "Cabeçalho 'cpfUsuario' é obrigatório."}, 400

        try:
            dto = CreateSuspeitoDTO.from_dict(data)
            dto.lastUpdateCpf = cpf_usuario  # ← atribui o CPF do usuário que criou
            result = self.create_suspeito_use_case.execute(dto)
            return result.to_dict(), 201
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500


class SuspeitoDetailController(Resource):
    def __init__(self, **kwargs):
        self.get_suspeito_by_id_use_case = kwargs['get_suspeito_by_id_use_case']

    def get(self, id: int):
        """
        Busca os dados detalhados de um suspeito pelo ID.
        ---
        tags:
          - Suspeito
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID do suspeito
        responses:
          200:
            description: Suspeito encontrado com sucesso
          404:
            description: Suspeito não encontrado
          500:
            description: Erro interno
        """
        try:
            suspeito = self.get_suspeito_by_id_use_case.execute(id)
            if not suspeito:
                return {"message": "Suspeito não encontrado"}, 404
            return suspeito.to_dict(), 200
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500
          
class CreateEmailController(Resource):
    def __init__(self, **kwargs):
        self.create_email_use_case: CreateEmailUseCase = kwargs['create_email_use_case']

    def post(self, id: int):
        """
        Busca os dados detalhados de um suspeito pelo ID.
        ---
        tags:
          - Suspeito
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID do suspeito
          - in: body
            required: true
            schema:
              type: object
              required:
                - email
              properties:
                email:
                  type: string
          - in: header
            name: cpfUsuario
            required: true
            schema:
              type: string
              example: "12345678900"
        responses:
          201:
            description: Email criado com sucesso
          400:
            description: Falha ao criar email
          500:
            description: Erro interno
        """
        try:
            data = request.get_json()
            cpf_usuario = request.headers.get("cpfUsuario")
            
            dto = CreateEmailDTO.from_dict(data, id, cpf_usuario)
            is_successful = self.create_email_use_case.execute(dto)
            
            if is_successful:
                return { "message": "Email criado com sucesso!" }, 201
            return { "message": "Falha ao criar email!" }, 400
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500

blueprint_suspeito = Blueprint('blueprint_suspeito', __name__)
api = Api(blueprint_suspeito)

api.add_resource(
    SuspeitoCreateController,
    "/suspeito",
    resource_class_kwargs={
        "create_suspeito_use_case": SuspeitoFactory.create_suspeito()
    }
)

api.add_resource(
    SuspeitoDetailController,
    "/suspeito/<int:id>",
    resource_class_kwargs={
        "get_suspeito_by_id_use_case": SuspeitoFactory.get_suspeito_by_id()
    }
)

api.add_resource(
    CreateEmailController,
    "/suspeito/<int:id>/email",
    resource_class_kwargs={
        "create_email_use_case": SuspeitoFactory.create_email()
    }
)