from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.application.usecases.exportusecase import ExportUseCase
from app.application.factories.exportfactory import ExportFactory
from app.infraestructure.utils.logger import logger

class ExportController(Resource):
    def __init__(self, **kwargs):
        self.export_use_case: ExportUseCase = kwargs['export_use_case']

    def post(self):
        """
        Exporta dados de suspeitos e mensagens com base em filtros.
        ---
        tags:
          - Exportação
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                numeros:
                  type: array
                  items:
                    type: string
                suspeitos:
                  type: array
                  items:
                    type: string
                operacoes:
                  type: array
                  items:
                    type: string
                grupo:
                  type: string
                  enum: [group, number, all]
                tipo:
                  type: string
                  enum: [image, audio, video, text, all]
                data_inicial:
                  type: string
                  format: date
                data_final:
                  type: string
                  format: date
                hora_inicio:
                  type: string
                hora_fim:
                  type: string
        responses:
          200:
            description: Arquivo ZIP gerado com sucesso
            content:
              application/zip:
                schema:
                  type: string
                  format: binary
          400:
            description: Requisição inválida
          500:
            description: Erro interno do servidor
        """
        try:
            data = request.get_json()

            numeros = [int(n) for n in data.get("numeros", [])]
            suspeitos = [int(s) for s in data.get("suspeitos", [])]
            operacoes = [str(o) for o in data.get("operacoes", [])]

            dto = MensagensRequestDTO.from_dict({
                "numeros": numeros,
                "suspeitos": suspeitos,
                "operacoes": operacoes,
                "grupo": data.get("grupo"),
                "tipo": data.get("tipo"),
                "data_inicial": data.get("data_inicial"),
                "data_final": data.get("data_final"),
                "hora_inicio": data.get("hora_inicio"),
                "hora_fim": data.get("hora_fim"),
            })

            return self.export_use_case.execute(dto)

        except Exception as e:
            logger.error(f"Erro ao exportar: {e}")
            return {"message": "Erro interno"}, 500

# Blueprint
blueprint_export = Blueprint("blueprint_export", __name__)
api = Api(blueprint_export)

api.add_resource(
    ExportController,
    "/exportar/csv",
    resource_class_kwargs={"export_use_case": ExportFactory.export_use_case()}
)
