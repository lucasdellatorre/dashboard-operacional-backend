from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.factories.mensagemipfactory import MensagemIpFactory
from app.application.usecases.buscarmensagemporipusecase import BuscarMensagemPorIPUseCase
from flask import request

class MensagemIPController(Resource):
    def __init__(self, **kwargs):
        self.buscar_mensagem_usecase: BuscarMensagemPorIPUseCase = kwargs["buscar_mensagem_usecase"]

    def get(self):
        """
        Consulta mensagens por IP com filtros.
        ---
        tags:
          - Mensagens
        parameters:
          - in: query
            name: numero
            required: true
            type: integer
          - in: query
            name: ips
            required: true
            type: array
            items:
              type: string
          - in: query
            name: grupo
            type: string
          - in: query
            name: tipo
            type: string
          - in: query
            name: dataInicial
            type: string
            format: date
          - in: query
            name: dataFinal
            type: string
            format: date
          - in: query
            name: horaInicial
            type: string
          - in: query
            name: horaFinal
            type: string
          - in: query
            name: diasSemana
            type: array
            items:
              type: integer
        responses:
          200:
            description: Lista de mensagens
          400:
            description: Erro de validação
          500:
            description: Erro interno
        """
        try:
            data = request.args.to_dict(flat=False)

            dto = MensagensRequestDTO.from_dict({
                "numeros": data.get("numeros", []) or data.get("numeros[]", []),
                "suspeitos": data.get("suspeitos", []) or data.get("suspeitos[]", []),
                "operacoes": data.get("operacoes", []) or data.get("operacoes[]", []),
                "grupo": request.args.get("grupo", "AMBOS"),
                "tipo": request.args.get("tipo", "TODOS"),
                "data_inicial": request.args.get("data_inicial"),
                "data_final": request.args.get("data_final"),
                "hora_inicio": request.args.get("hora_inicio"),
                "hora_fim": request.args.get("hora_fim"),
            })

            mensagens_response = self.buscar_mensagem_usecase.execute(dto)
            return [m.to_dict() for m in mensagens_response], 200

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