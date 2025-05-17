from flask import Blueprint
from app.application.factories.suspeitofactory import SuspeitoFactory
from flask_restful import Api, Resource
from app.application.usecases.getsuspeitobyidusecase import GetSuspeitoByIdUseCase

class SuspeitoController(Resource):
    def __init__(self, **kwargs):
        self.get_suspeito_by_id_use_case: GetSuspeitoByIdUseCase = kwargs['get_suspeito_by_id_use_case']

    def get(self, id: int):
        """
        Retorna os dados detalhados de um suspeito por ID.
        ---
        tags:
          - Suspeito
        parameters:
          - name: id
            in: path
            required: true
            schema:
              type: integer
            description: ID do suspeito
        responses:
          200:
            description: Suspeito encontrado
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                    nome:
                      type: string
                    apelido:
                      type: string
                    cpf:
                      type: string
                    relevante:
                      type: boolean
                    anotacoes:
                      type: string
                    emails:
                      type: array
                      items:
                        type: string
                    celulares:
                      type: array
                      items:
                        type: string
                    ips:
                      type: array
                      items:
                        type: string
          404:
            description: Suspeito não encontrado
          500:
            description: Erro interno no servidor
        """
        try:
            suspeito = self.get_suspeito_by_id_use_case.execute(id)
            if suspeito is None:
                return {"message": "Suspeito não encontrado"}, 404

            return suspeito.to_dict(), 200

        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500

# Blueprint e registro
blueprint_suspeito = Blueprint('blueprint_suspeito', __name__)
api = Api(blueprint_suspeito)

api.add_resource(
    SuspeitoController,
    '/suspeito/<int:id>',
    resource_class_kwargs={
        'get_suspeito_by_id_use_case': SuspeitoFactory.get_suspeito_by_id()
    }
)
