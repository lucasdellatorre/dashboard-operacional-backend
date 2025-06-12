from flask import Blueprint, request, send_file, jsonify
from flask_restful import Api, Resource
from io import BytesIO
from zipfile import ZipFile
import traceback

from app.application.dto.filtrodto import FiltroDTO
from app.application.factories.exportfactory import ExportFactory
from app.domain.services.exportservice import ExportService
from app.infraestructure.utils.logger import logger

class ExportCSVController(Resource):
    def __init__(self, **kwargs):
        self.export_service = kwargs["export_service"]

    def get(self):
        try:
            numero = request.args.getlist("numero")
            operacoes = request.args.getlist("operacoes")
            grupo = request.args.get("grupo")
            tipo = request.args.get("tipo")
            data_inicial = request.args.get("data_inicial")
            data_final = request.args.get("data_final")
            hora_inicial = request.args.get("hora_inicial")
            hora_final = request.args.get("hora_final")
            dias_semana = request.args.getlist("dias_semana", type=int)

            filtro_dto = FiltroDTO(
                numero=numero,
                operacoes=operacoes,
                grupo=grupo,
                tipo=tipo,
                data_inicial=data_inicial,
                data_final=data_final,
                hora_inicial=hora_inicial,
                hora_final=hora_final,
                dias_semana=dias_semana
            )

            csv_suspeitos, csv_mensagens_ligacoes = self.export_service.gerar_csvs(filtro_dto)

            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, "w") as zip_file:
                zip_file.writestr("suspeitos.csv", csv_suspeitos)
                zip_file.writestr("mensagens_ligacoes.csv", csv_mensagens_ligacoes)

            zip_buffer.seek(0)
            return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='export_teia.zip')

        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {e}")
            traceback.print_exc()
            return jsonify({"message": "Erro interno ao exportar os arquivos"}), 500


# Blueprint
blueprint_export = Blueprint("blueprint_export", __name__)
api = Api(blueprint_export)

api.add_resource(
    ExportCSVController,
    "/exportar/csv",
    resource_class_kwargs={"export_service": ExportFactory.build_export_service()}
)