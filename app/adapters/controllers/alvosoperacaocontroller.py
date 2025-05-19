from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.usecases.getoperationtargetsusecase import GetOperationTargetsUseCase
from app.application.factories.listaalvosoperacaofactory import ListaAlvosOperacaoFactory

# Controller 1 - /numeros/operacao/<ids>
class AlvosOperacaoController(Resource):
    def __init__(self, **kwargs):
        self.lista_numero: GetOperationTargetsUseCase = kwargs['lista_operacoes']

    def get(self, operacao_ids=None):
        """
        Retorna a lista de números e suspeitos vinculados às operações informadas.
        Se nenhum ID for informado, retorna todos os dados.
        """
        try:
            operacao_id_list = []

            if operacao_ids:
                operacao_id_list = [
                    int(op_id.strip()) for op_id in operacao_ids.split(',') if op_id.strip().isdigit()
                ]

            resultado = self.lista_numero.execute(operacao_id_list)

            if not resultado:
                return {"message": "Nenhum dado encontrado para as operações informadas."}, 404

            return resultado, 200

        except Exception as e:
            print(f'[ERRO /numeros/operacao]: {e}')
            return {'message': 'Erro interno no servidor.'}, 500

        
blueprint_numeros_operacao = Blueprint('blueprint_numeros_operacao', __name__)
api = Api(blueprint_numeros_operacao)

api.add_resource(
    AlvosOperacaoController,
    '/numeros/operacao/',
    '/numeros/operacao/<string:operacao_ids>',
    resource_class_kwargs={
        'lista_operacoes': ListaAlvosOperacaoFactory.listar()
    }
)