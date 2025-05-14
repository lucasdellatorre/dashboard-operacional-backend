from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from app.application.dto.numeromessagecountdto import NumeroMessageCountRequestDTO
from app.application.factories.teiafactory import TeiaFactory
from app.application.usecases.teiamessagecount import TeiaMessageCountUseCase
from app.infraestructure.utils.logger import logger

class TeiaController(Resource):
    def __init__(self, **kwargs):
        self.teia_msg_use_case: TeiaMessageCountUseCase = kwargs['teia_msg_count_use_case']
        self.req_parser = reqparse.RequestParser()

    def post(self):
        """
        Retorna a contagem de mensagens da teia com base nos parâmetros fornecidos.
        ---
        tags:
          - Teia
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                numero:
                  type: string
                  description: Número para buscar a contagem de mensagens
                dataInicial:
                  type: string
                  format: date
                  description: Data inicial do filtro (formato yyyy-mm-dd)
                dataFinal:
                  type: string
                  format: date
                  description: Data final do filtro (formato yyyy-mm-dd)
        responses:
          200:
            description: Contagem de mensagens retornada com sucesso
            schema:
              type: object
              properties:
                count:
                  type: integer
                  description: Número total de mensagens encontradas
          400:
            description: Erro de validação nos parâmetros fornecidos
          500:
            description: Erro interno no servidor
        """
        data = request.get_json()
        try:
            intercept_upload_dto = NumeroMessageCountRequestDTO(**data)
            result = self.teia_msg_use_case.execute(intercept_upload_dto)
            return result.to_dict(), 200
        except ValueError as e:
            return {'Message': f'{e}'}, 400
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500

blueprint_teia = Blueprint('blueprint_teia', __name__)
api = Api(blueprint_teia)

api.add_resource(
    TeiaController,
    '/teia/message',
    resource_class_kwargs={'teia_msg_count_use_case': TeiaFactory.message_count()}
)