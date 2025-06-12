# teiaipcontroller.py
from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.dto.teiaipmessagecountdto import TeiaIPMessageCountRequestDTO
from app.application.usecases.teiaipmessagecountusecase import TeiaIPMessageCountUseCase
from app.application.factories.teiaipfactory import TeiaIPFactory
from app.infraestructure.utils.logger import logger

class TeiaIPController(Resource):
    def __init__(self, **kwargs):
        self.teia_ip_msg_use_case = kwargs['teia_ip_msg_use_case']

    def get(self):
        """
        Retorna um grafo com nodos e links com base em IPs e mensagens.
        ---
        tags:
          - TeiaIP
        parameters:
          - in: query
            name: ids
            required: true
            type: string
        responses:
          200:
            description: Grafo gerado com sucesso
          400:
            description: Erro de validação
          500:
            description: Erro interno
        """
        try:
            ids_param = request.args.get('ids')
            if not ids_param:
                return {'Message': "Missing 'ids' query parameter"}, 400

            ip_ids = [int(x.strip()) for x in ids_param.split(',')]
            request_dto = TeiaIPMessageCountRequestDTO(ip_ids=ip_ids)
            result = self.teia_ip_msg_use_case.execute(request_dto)
            return result.to_dict(), 200
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500

blueprint_teia_ip = Blueprint('blueprint_teia_ip', __name__)
api = Api(blueprint_teia_ip)
api.add_resource(
    TeiaIPController,
    '/teia/ip-message',
    resource_class_kwargs={'teia_ip_msg_use_case': TeiaIPFactory.message_count()}
)
