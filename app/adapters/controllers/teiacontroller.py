from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.factories.teiafactory import TeiaFactory
from app.application.usecases.teiamessagecount import TeiaMessageCountUseCase
from app.infraestructure.utils.logger import logger
import time

class TeiaController(Resource):
    def __init__(self, **kwargs):
        self.teia_msg_use_case: TeiaMessageCountUseCase = kwargs['teia_msg_count_use_case']
        self.req_parser = reqparse.RequestParser()

    def get(self):
        """
        Retorna a contagem de mensagens da teia com base nos parâmetros fornecidos.
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
          - name: grupo
            in: query
            required: false
            schema:
              type: string
              enum: [group, number, all]
          - name: tipo
            in: query
            required: false
            schema:
              type: string
              enum: [image, audio, video, text, all]
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
        start_time = time.time()
        try:
            data = request.args.to_dict(flat=False)
            dto = MensagensRequestDTO.from_dict({
                "numeros": data.get("numeros", []) or data.get("numeros[]", []),
                "suspeitos": data.get("suspeitos", []) or data.get("suspeitos[]", []),
                "operacoes": data.get("operacoes", []) or data.get("operacoes[]", []),
                "grupo": request.args.get("grupo"),
                "tipo": request.args.get("tipo"),
                "data_inicial": request.args.get("data_inicial"),
                "data_final": request.args.get("data_final"),
                "hora_inicio": request.args.get("hora_inicio"),
                "hora_fim": request.args.get("hora_fim"),
            })
          
            result = self.teia_msg_use_case.execute(dto)
            return result.to_dict(), 200

        except ValueError as e:
            return {'Message': f'{e}'}, 400
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500
        finally:
            duration_ms = (time.time() - start_time) * 1000
            print(f'[INFO /mensagens] Tempo de execução: {duration_ms:.2f} ms')
        

blueprint_teia = Blueprint('blueprint_teia', __name__)
api = Api(blueprint_teia)

api.add_resource(
    TeiaController,
    '/teia/message',
    resource_class_kwargs={'teia_msg_count_use_case': TeiaFactory.message_count()}
)