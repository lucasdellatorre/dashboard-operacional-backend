from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from app.infraestructure.utils.progress_tracker import get_progress, get_all_pending_jobs

# Recurso para obter o progresso de um job específico
class UploadProgressDetail(Resource):
    def get(self, job_id):
        """
        Consulta o progresso atual de um job de upload.

        ---
        tags:
          - Upload
        parameters:
          - name: job_id
            in: path
            type: string
            required: true
            description: ID do job de upload
        responses:
          200:
            description: Status do progresso do upload
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "Processando Planilha 2"
                progress:
                  type: integer
                  example: 75
                erro:
                  type: boolean
                  example: false
                mensagem:
                  type: string
                  example: null
        """
        progress = get_progress(job_id)
        if progress["status"] == "not found":
            return make_response(jsonify(progress), 404)
        return jsonify(progress)


# Recurso para listar todos os jobs pendentes
class UploadProgressList(Resource):
    def get(self):
        """
        Retorna todos os jobs de upload pendentes.

        ---
        tags:
          - Upload
        responses:
          200:
            description: Lista de jobs pendentes
            schema:
              type: array
              items:
                type: object
                properties:
                  job_id:
                    type: string
                  nome:
                    type: string
                  size:
                    type: integer
                  data_upload:
                    type: string
        """
        jobs = get_all_pending_jobs()
        return jsonify(jobs)


# Blueprint e registro dos endpoints
blueprint_progress = Blueprint('blueprint_progress', __name__)
api = Api(blueprint_progress)

api.add_resource(UploadProgressDetail, '/upload/progresso/<string:job_id>')
api.add_resource(UploadProgressList, '/upload/progresso')
