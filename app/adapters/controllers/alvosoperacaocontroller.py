from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.usecases.getoperationtargetsusecase import GetOperationTargetsUseCase
from app.application.factories.listaalvosoperacaofactory import ListaAlvosOperacaoFactory

# Controller 1 - /numeros/operacao/<ids>
class AlvosOperacaoController(Resource):
    def __init__(self, **kwargs):
        self.lista_numero: GetOperationTargetsUseCase = kwargs['lista_operacoes']

    def get(self, operacao_ids):
        """
        Retorna a lista de números vinculados às operações informadas.
        ---
        tags:
          - Números
        parameters:
          - name: operacao_ids
            in: path
            required: true
            schema:
              type: string
            description: "Lista de IDs de operação separados por vírgula (ex: 1,2,3)"
        responses:
          200:
            description: Lista de números vinculados às operações.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
          400:
            description: IDs inválidos
          404:
            description: Nenhum dado encontrado
          500:
            description: Erro interno
        """
        try:
            operacao_id_list = [int(op_id.strip()) for op_id in operacao_ids.split(',') if op_id.strip().isdigit()]
            if not operacao_id_list:
                return {"message": "IDs de operação inválidos ou não fornecidos."}, 400

            numeros = self.lista_numero.execute(operacao_id_list)
            if not numeros:
                return {"message": "Nenhum dado encontrado para as operações informadas."}, 404

            return [numero.to_dict() for numero in numeros], 200

        except Exception as e:
            print(f'[ERRO /numeros/operacao]: {e}')
            return {'message': 'Erro interno no servidor.'}, 500
        
blueprint_numeros_operacao = Blueprint('blueprint_numeros_operacao', __name__)
api = Api(blueprint_numeros_operacao)

api.add_resource(
    AlvosOperacaoController,
    '/numeros/operacao/<string:operacao_ids>',
    resource_class_kwargs={
        'lista_operacoes': ListaAlvosOperacaoFactory.listar()
    }
)        