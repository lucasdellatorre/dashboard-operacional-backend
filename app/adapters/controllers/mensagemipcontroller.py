from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.factories.mensagemipfactory import MensagemIpFactory
from app.application.usecases.buscarmensagemporipusecase import BuscarMensagemPorIPUseCase

class MensagemIPController(Resource):
    def __init__(self, **kwargs):
        self.buscar_mensagem_usecase: BuscarMensagemPorIPUseCase = kwargs["buscar_mensagem_usecase"]

    def get(self):
        """
        Retorna a quantidade de mensagens por IP com filtros.
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
            description: Lista de IPs com a quantidade de mensagens.
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
            print(f"[Erro] /mensagens/ip: {e}")
            return {"message": "Erro interno no servidor."}, 500

blueprint_mensagem_ip = Blueprint("blueprint_mensagem_ip", __name__)
api = Api(blueprint_mensagem_ip)

api.add_resource(
    MensagemIPController,
    "/mensagens/ip",
    resource_class_kwargs={
        "buscar_mensagem_usecase": MensagemIpFactory.buscar_mensagens_por_ip()
    }
)