from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.factories.operacaofactory import OperacaoFactory
from app.application.usecases.createoperacaousecase import CreateOperacaoUseCase
from app.application.usecases.getalloperacaousecase import GetAllOperacaoUseCase
from app.application.dto.operacaodto import OperacaoDTO

class OperacaoController(Resource):
    def __init__(self, **kwargs):
        self.create_operacao_use_case: CreateOperacaoUseCase = kwargs['create_operacao_use_case']
        self.get_all_operacao_use_case: GetAllOperacaoUseCase = kwargs['get_all_operacao_use_case']
        self.req_parser = reqparse.RequestParser()

    def post(self):
        """
        Cria uma nova operação.
        ---
        tags:
          - Operação
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  description: Nome da operação
        responses:
          201:
            description: Operação criada com sucesso
            schema:
              type: object
              properties:
                Operacao:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: ID da operação
                    nome:
                      type: string
                      description: Nome da operação
          400:
            description: Erro de validação dos parâmetros
          500:
            description: Erro interno no servidor
        """
        self.req_parser.add_argument('nome', required=True, location='json')
        
        args = self.req_parser.parse_args()
        
        try:
            target_dto = OperacaoDTO(**args)
            target = self.create_operacao_use_case.execute(target_dto)
            return target.to_dict(), 201
        except ValueError as ve:
            return {'Message': f'{ve}'}, 400
        except Exception as e:
            print(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500

    def get(self):
        """
        Retorna todas as operações cadastradas.
        ---
        tags:
          - Operação
        responses:
          200:
            description: Lista de operações
            schema:
              type: object
              properties:
                Operacao:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: ID da operação
                      nome:
                        type: string
                        description: Nome da operação
          500:
            description: Erro interno no servidor
        """
        try:
            operacoes = self.get_all_operacao_use_case.execute()
            return [operacao.to_dict() for operacao in operacoes], 200
        except Exception as e:
            print(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500

blueprint_operacao = Blueprint('blueprint_operacao', __name__)
api = Api(blueprint_operacao)

api.add_resource(
    OperacaoController,
    '/operacao',
    resource_class_kwargs={
        'create_operacao_use_case': OperacaoFactory.create_operacao(),
        'get_all_operacao_use_case': OperacaoFactory.get_all_operacao()
    }
)