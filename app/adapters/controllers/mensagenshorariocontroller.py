from flask_restful import Api, Resource
from flask import Blueprint, request
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.usecases.getmensagensporhorariousecase import GetMensagensPorHorarioUseCase
from app.application.factories.mensagenshorariofactory import MensagensHorarioFactory
import time

class MensagensHorarioController(Resource):
    def __init__(self, **kwargs):
        self.usecase: GetMensagensPorHorarioUseCase = kwargs['get_mensagens_por_horario']

    def get(self):
        """
        Retorna a quantidade de mensagens agrupadas por faixa de horário de 2 horas.
        ---
        tags:
          - Mensagens
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
            required: true
            schema:
              type: array
              items:
                type: string
          - name: grupo
            in: query
            required: false
            schema:
              type: string
              enum: [GRUPO, NÚMERO, AMBOS]
          - name: tipo
            in: query
            required: false
            schema:
              type: string
              enum: [TEXTO, VÍDEO, TODOS]
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
              example: "08:00"
          - name: hora_fim
            in: query
            required: false
            schema:
              type: string
              example: "18:00"
        responses:
          200:
            description: Lista de faixas de horário com a quantidade de mensagens.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      periodo:
                        type: string
                        example: "08:00-10:00"
                      qtdMensagens:
                        type: integer
                        example: 42
          400:
            description: Parâmetros inválidos
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

            resultado = self.usecase.execute(dto)
            return resultado, 200

        except ValueError as ve:
            return {'message': str(ve)}, 400
        except Exception as e:
            print(f'[ERRO /mensagens/horario]: {e}')
            return {'message': 'Erro interno no servidor.'}, 500
        finally:
            duration_ms = (time.time() - start_time) * 1000
            print(f'[INFO /mensagens/horario] Tempo de execução: {duration_ms:.2f} ms')

# Blueprint e rota
blueprint_mensagens_horario = Blueprint('blueprint_mensagens_horario', __name__)
api = Api(blueprint_mensagens_horario)

api.add_resource(
    MensagensHorarioController,
    '/mensagens/horario',
    resource_class_kwargs={
        'get_mensagens_por_horario': MensagensHorarioFactory.get_mensagens_por_horario()
    }
)