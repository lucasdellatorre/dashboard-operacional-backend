from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.dto.patchnumerosuspeitodto import PatchNumeroSuspeitoDTO
from app.application.usecases.adicionanumerosuspeitousecase import AdicionaNumeroSuspeitoUseCase
from app.application.usecases.getallnumbersusecase import GetAllNumbersUseCase
from app.application.factories.listanumerofactory import ListaNumerosFactory
from app.application.factories.adicionanumerosuspeitofactory import AdicionaNumeroSuspeitoFactory
import time

class NumeroController(Resource):
    def __init__(self, **kwargs):
        self.get_all_numeros: GetAllNumbersUseCase = kwargs['get_all_numeros']
        self.adicionar_numeros_suspeito: AdicionaNumeroSuspeitoUseCase = kwargs['adicionar_numeros_suspeito']

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

    def patch(self):
        """
        Adiciona celulares ao suspeito
        ---
        tags:
          - Números
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  cpf:
                    type: string
                  suspeito_id:
                    type: integer
                  id_numeros:
                    type: array
                    items:
                      type: integer
        responses:
          200:
            description: Lista de telefones do suspeito.
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
          400:
            description: Dados inválidos
          404:
            description: Número não encontrado ou não é alvo
          500:
            description: Erro interno no servidor
        """
        
        data = request.get_json()
        start_time = time.time()
        try:
            numero_suspeito_dto = PatchNumeroSuspeitoDTO(**data)
            result = self.adicionar_numeros_suspeito.execute(numero_suspeito_dto)
            return result.to_dict(), 200
        except ValueError as ve:
            return {'message': str(ve)}, 404
        except Exception as e:
            print(f'[ERRO PATCH /numeros]: {e}')
            return {'message': 'Erro interno no servidor.'}, 500
        finally:
            duration_ms = (time.time() - start_time) * 1000
            print(f'[INFO PATCH /numeros] Tempo de execução: {duration_ms:.2f} ms')

blueprint_numero = Blueprint('blueprint_numero', __name__)
api = Api(blueprint_numero)

api.add_resource(
    NumeroController,
    '/numeros',
    resource_class_kwargs={
        'get_all_numeros': ListaNumerosFactory.listar(),
        'adicionar_numeros_suspeito': AdicionaNumeroSuspeitoFactory.criar()
    }
)