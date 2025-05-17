from flask import Blueprint
from flask_restful import Api, Resource
from app.application.usecases.listanumerousercase import ListarNumeroUseCase
from app.application.factories.listanumerofactory import ListaNumeroFactory  

class NumeroController(Resource):
    def __init__(self, **kwargs):
        self.lista_numero: ListarNumeroUseCase = kwargs['lista_operacoes']

    def get(self, operacao_ids):
        """
         Retorna a lista de números vinculados às operações informadas.
        ---
        parameters:
          - name: operacao_ids
            in: path
            type: string
            required: true
            description: Lista de IDs de operação separados por vírgula (exemplo: 1,2,3)
        responses:
          200:
            description: Lista de números vinculados às operações.
            schema:
              type: array
              items:
                type: object
          400:
            description: IDs de operação inválidos ou não fornecidos.
          404:
            description: Nenhum dado encontrado para as operações informadas.
          500:
            description: Erro interno no servidor.
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
            print(f'An error occurred: {e}')
            return {'message': 'Erro interno no servidor.'}, 500


blueprint_numero = Blueprint('blueprint_numero', __name__)


api = Api(blueprint_numero)
api.add_resource(NumeroController,'/numeros/operacao/<string:operacao_ids>',resource_class_kwargs={'lista_operacoes': ListaNumeroFactory.listar_numero()})
