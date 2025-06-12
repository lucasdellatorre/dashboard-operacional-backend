from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.factories.mensagemdiafactory import MensagemDiaFactory
from app.application.usecases.buscarmensagempordiausecase import BuscarMensagemPorDiaUseCase

class MensagemDiaController(Resource):
    def __init__(self, **kwargs):
        self.buscar_mensagem_usecase: BuscarMensagemPorDiaUseCase = kwargs["buscar_mensagem_usecase"]

    def get(self):
        """
        Retorna a quantidade de mensagens por dia da semana
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
            description: Lista de dias com a quantidade de mensagens.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      value:
                        type: integer
          400:
            description: Parâmetros inválidos
          500:
            description: Erro interno no servidor
        """
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
          
            result = self.buscar_mensagem_usecase.execute(dto)
            return result, 200

        except Exception as e:
            print(f"[Erro] /mensagens/dia: {e}")
            return {"message": "Erro interno no servidor."}, 500

blueprint_mensagem_dia = Blueprint("blueprint_mensagem_dia", __name__)
api = Api(blueprint_mensagem_dia)

api.add_resource(
    MensagemDiaController,
    "/mensagens/dia",
    resource_class_kwargs={
        "buscar_mensagem_usecase": MensagemDiaFactory.buscar_mensagens_por_dia()
    }
)