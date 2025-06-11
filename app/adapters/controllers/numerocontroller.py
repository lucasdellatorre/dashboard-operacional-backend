import time
from flask import Blueprint
from flask_restful import Api, Resource
from app.application.usecases.getallnumbersusecase import GetAllNumbersUseCase
from app.application.factories.listanumerofactory import ListaNumerosFactory

class NumeroController(Resource):
    def __init__(self, **kwargs):
        self.get_all_numeros: GetAllNumbersUseCase = kwargs['get_all_numeros']

    def get(self):
        """
        Retorna todos os números
        ---
        tags:
          - Números
        responses:
          200:
            description: Lista de números interceptados.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      numero:
                        type: string
          500:
            description: Erro interno no servidor
        """
        start_time = time.time()
        try:
            numeros = self.get_all_numeros.execute()
            return numeros, 200

        except Exception as e:
            print(f'[ERRO /numeros]: {e}')
            return {'message': 'Erro interno no servidor.'}, 500

        finally:
            duration_ms = (time.time() - start_time) * 1000
            print(f'[INFO /numeros] Tempo de execução: {duration_ms:.2f} ms')

blueprint_numero = Blueprint('blueprint_numero', __name__)
api = Api(blueprint_numero)

api.add_resource(
    NumeroController,
    '/numeros',
    resource_class_kwargs={
        'get_all_numeros': ListaNumerosFactory.listar(),
    }
)