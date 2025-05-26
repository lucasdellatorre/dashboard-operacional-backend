from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.factories.mensagemipfactory import MensagemIpFactory
from app.application.usecases.buscarmensagemporipusecase import BuscarMensagemPorIPUseCase
from app.application.dto.filtromensagemdto import FiltroMensagemDTO

class MensagemIPController(Resource):
    def __init__(self, **kwargs):
        self.buscar_mensagem_usecase: BuscarMensagemPorIPUseCase = kwargs["buscar_mensagem_usecase"]
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument("numero", required=True, type=int, location="args")
        self.req_parser.add_argument("ips", required=True, action="append", location="args")
        self.req_parser.add_argument("grupo", type=str, location="args")
        self.req_parser.add_argument("tipo", type=str, location="args")
        self.req_parser.add_argument("dataInicial", type=str, location="args")
        self.req_parser.add_argument("dataFinal", type=str, location="args")
        self.req_parser.add_argument("horaInicial", type=str, location="args")
        self.req_parser.add_argument("horaFinal", type=str, location="args")
        self.req_parser.add_argument("diasSemana", action="append", type=int, location="args")

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
            args = self.req_parser.parse_args()

            if not args["ips"] or len(args["ips"]) == 0:
                return {"message": "Informe ao menos um IP."}, 400

            filtro_dto = FiltroMensagemDTO(
                numero=args["numero"],
                ips=args["ips"],
                grupo=args.get("grupo"),
                tipo=args.get("tipo"),
                data_inicial=args.get("dataInicial"),
                data_final=args.get("dataFinal"),
                hora_inicial=args.get("horaInicial"),
                hora_final=args.get("horaFinal"),
                dias_semana=args.get("diasSemana"),
            )

            mensagens_response = self.buscar_mensagem_usecase.execute(filtro_dto)
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