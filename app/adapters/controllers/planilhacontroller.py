from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.usecases.getallplanilhausecase import GetAllPlanilhaUseCase
from app.application.factories.planilhafactory import PlanilhaFactory

class PlanilhaController(Resource):
    def __init__(self, **kwargs):
        self.get_all_planilha_use_case: GetAllPlanilhaUseCase = kwargs['get_all_planilha_use_case']
        self.req_parser = reqparse.RequestParser()
    
    def get(self):
        """
        Retorna a lista de planilhas por ordem de inserção.
        ---
        tags:
          - Planilha
        responses:
          200:
            description: Lista de planilhas por ordem de inserção
            schema:
              type: object
              properties:
                Planilhas:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: ID da planilha
                      nome:
                        type: string
                        description: Nome do arquivo da planilha
                      data_upload:
                        type: date
                        description: Data de upload da planilha
                      size:
                        type: integer
                        description: Tamanho do arquivo da planilha KB
          500:
            description: Erro interno do servidor
        """
        try:
            planilhas = self.get_all_planilha_use_case.execute()
            return {'Planilhas': [planilha.to_dict() for planilha in planilhas]}, 200
        except Exception as e:
            print(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500

blueprint_planilha = Blueprint('blueprint_planilha', __name__)
api = Api(blueprint_planilha)

api.add_resource(
    PlanilhaController,
    '/planilha',
    resource_class_kwargs={'get_all_planilha_use_case': PlanilhaFactory.get_all_Planilha()}
)
