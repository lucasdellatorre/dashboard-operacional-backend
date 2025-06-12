# teiaipcontroller.py
from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.dto.teiaipmessagecountdto import TeiaIPMessageCountRequestDTO
from app.application.usecases.teiaipmessagecountusecase import TeiaIPMessageCountUseCase
from app.application.factories.teiaipfactory import TeiaIPFactory
from app.infraestructure.utils.logger import logger

class TeiaIPController(Resource):
    def __init__(self, **kwargs):
        self.teia_ip_msg_use_case: TeiaIPMessageCountUseCase = kwargs['teia_ip_msg_use_case']

    def get(self):
        """
        Retorna a contagem de mensagens da teia por ip com base nos parâmetros fornecidos.
        ---
        tags:
          - Teia
        parameters:
          - name: numeros
            in: query
            required: false
            schema:
              type: array
              items:
                type: string
          - name: suspeitos
            in: query
            required: false
            schema:
              type: array
              items:
                type: string
          - name: operacoes
            in: query
            required: false
            schema:
              type: array
              items:
                type: string
          - name: data_inicial
            in: query
            required: false
            schema:
              type: string
              format: date
          - name: data_final
            in: query
            required: false
            schema:
              type: string
              format: date
          - name: hora_inicio
            in: query
            required: false
            schema:
              type: string
          - name: hora_fim
            in: query
            required: false
            schema:
              type: string
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
        try:
            data = request.args.to_dict(flat=False)
            dto = TeiaIPMessageCountRequestDTO.from_dict({
                "numeros": data.get("numeros", []) or data.get("numeros[]", []),
                "suspeitos": data.get("suspeitos", []) or data.get("suspeitos[]", []),
                "operacoes": data.get("operacoes", []) or data.get("operacoes[]", []),
                "data_inicial": request.args.get("data_inicial"),
                "data_final": request.args.get("data_final"),
                "hora_inicio": request.args.get("hora_inicio"),
                "hora_fim": request.args.get("hora_fim"),
            })
            
            result = self.teia_ip_msg_use_case.execute(dto)
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
