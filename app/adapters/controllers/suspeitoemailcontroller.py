from flask import request
from flask_restful import Resource
from app.application.dto.updateemaildto import UpdateEmailDTO
from app.application.usecases.updateemailusecase import UpdateEmailUseCase
from app.application.usecases.deleteemailusecase import DeleteEmailUseCase
from flask import Blueprint
from flask_restful import Api
from app.application.factories.suspeitofactory import SuspeitoFactory

from flask import request
from flask_restful import Resource
from app.application.dto.createemaildto import CreateEmailDTO
from app.application.usecases.getallemailusecase import GetAllEmailUseCase
from app.application.usecases.createemailusecase import CreateEmailUseCase

class SuspeitoEmailListController(Resource):
    def __init__(self, **kwargs):
        self.get_all_email_use_case: GetAllEmailUseCase = kwargs['get_all_email_use_case']
        self.create_email_use_case: CreateEmailUseCase = kwargs['create_email_use_case']

    def get(self, id: int):
        """
        Retorna os emails de um suspeito.
        ---
        tags:
          - SuspeitoEmail
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID do suspeito
        responses:
          200:
            description: Lista de emails retornada com sucesso.
        """
        try:
            results = self.get_all_email_use_case.execute(id)
            return {"emails": [result.to_dict() for result in results]}, 200
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500

    def post(self, id: int):
        """
        Adiciona um email ao suspeito identificado pelo ID.
        ---
        tags:
          - SuspeitoEmail
        consumes:
          - application/json
        parameters:
          - in: path
            name: id
            required: true
            description: ID do suspeito
            schema:
              type: integer
          - in: header
            name: cpfUsuario
            required: true
            description: CPF do usuário autenticado
            schema:
              type: string
              example: "12345678900"
          - in: body
            name: body
            description: Payload para criar email
            required: true
            schema:
              type: object
              required:
                - email
              properties:
                email:
                  type: string
                  example: "exemplo@dominio.com"
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
            success = self.create_email_use_case.execute(dto)

            if success:
                return {"message": "Email criado com sucesso!"}, 201
            return {"message": "Falha ao criar email!"}, 400
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500


class SuspeitoEmailDetailController(Resource):
    def __init__(self, **kwargs):
        self.update_email_use_case: UpdateEmailUseCase = kwargs['update_email_use_case']
        self.delete_email_use_case: DeleteEmailUseCase = kwargs['delete_email_use_case']

    def put(self, id: int, emailId: int):
        """
        Atualiza um email existente de um suspeito.
        ---
        tags:
          - SuspeitoEmail
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
          - in: path
            name: emailId
            required: true
            schema:
              type: integer
          - in: header
            name: cpfUsuario
            required: true
            schema:
              type: string
          - in: body
            name: body
            description: Payload para criar email
            required: true
            schema:
              type: object
              required:
                - email
              properties:
                email:
                  type: string
                  example: "exemplo@dominio.com"
        responses:
          200:
            description: Email atualizado com sucesso
          400:
            description: Erro de validação
          404:
            description: Email não encontrado
        """
        try:
            data = request.get_json()
            cpf_usuario = request.headers.get("cpfUsuario")

            dto = UpdateEmailDTO.from_dict(data, emailId, cpf_usuario)
            email = self.update_email_use_case.execute(dto)

            return email.to_dict(), 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except LookupError:
            return {"message": "Email não encontrado."}, 404
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500

    def delete(self, id: int, emailId: int):
        """
        Remove um email de um suspeito.
        ---
        tags:
          - SuspeitoEmail
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
          - in: path
            name: emailId
            required: true
            schema:
              type: integer
        responses:
          200:
            description: Email deletado com sucesso
          400:
            description: Falha ao deletar
        """
        try:
            success = self.delete_email_use_case.execute(id, emailId)

            if success:
                return {"message": "Email deletado com sucesso!"}, 200
            return {"message": "Falha ao deletar email!"}, 400
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500


blueprint_suspeito_email = Blueprint('blueprint_suspeito_email', __name__)
api = Api(blueprint_suspeito_email)

api.add_resource(
    SuspeitoEmailListController,
    "/suspeito/<int:id>/email",
    resource_class_kwargs={
        "get_all_email_use_case": SuspeitoFactory.get_all_email(),
        "create_email_use_case": SuspeitoFactory.create_email()
    }
)

api.add_resource(
    SuspeitoEmailDetailController,
    "/suspeito/<int:id>/email/<int:emailId>",
    resource_class_kwargs={
        "update_email_use_case": SuspeitoFactory.update_email(),
        "delete_email_use_case": SuspeitoFactory.delete_email()
    }
)