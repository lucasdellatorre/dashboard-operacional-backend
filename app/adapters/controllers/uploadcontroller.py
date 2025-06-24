import werkzeug
import uuid
from flask import current_app, Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.dto.interceptacaouploaddto import InterceptacaoUploadDTO
from app.application.factories.uploadfactory import UploadInterceptacaoFactory
from app.application.usecases.interceptacaouploadusecase import InterceptacaoUploadUseCase
from app.infraestructure.utils.logger import logger
from app.infraestructure.utils.progress_tracker import set_job_metadata
from datetime import datetime

class InterceptacaoUploadController(Resource):
    def __init__(self, **kwargs):
        self.intercept_upload_use_case: InterceptacaoUploadUseCase = kwargs['intercept_upload_use_case']
        self.req_parser = reqparse.RequestParser()

    def post(self):
        """
        Faz o upload de uma planilha de interceptação.

        ---
        tags:
        - Upload
        consumes:
        - multipart/form-data
        parameters:
        - name: file
          in: formData
          type: file
          required: true
          description: Arquivo da planilha (.xlsx, .xls, etc.)
        - name: operacaoId
          in: formData
          type: string
          required: true
          description: ID da operação vinculada ao upload
        responses:
          202:
            description: Upload iniciado com sucesso
            schema:
              type: object
              properties:
                job_id:
                  type: string
                  example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
          400:
            description: Erro de validação
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "operation id does not exist!"
          500:
            description: Erro interno
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Internal Server Error"
        """
        self.req_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        self.req_parser.add_argument('operacaoId', location='form')
        args = self.req_parser.parse_args()

        dto = InterceptacaoUploadDTO(**args)

        try:
            # Valida antes de criar o job
            logger.info(f"[UPLOAD] Operação ID: {dto.operacao_id}")
            self.intercept_upload_use_case.validate(dto)
        except ValueError as e:
            logger.warning(f"[UPLOAD] Validação falhou: {e}")
            return {'message': str(e)}, 400

        try:
            job_id = str(uuid.uuid4())

            file = dto.file
            file.stream.seek(0, 2)  # Vai para o final do arquivo
            size = file.stream.tell()
            file.stream.seek(0)     # Retorna para o início (IMPORTANTE)

            set_job_metadata(
                job_id,
                nome=file.filename,
                size=size,
                data_upload=datetime.utcnow().strftime("%Y-%m-%d")
            )
            
            logger.info(f"[UPLOAD] Arquivo recebido: {dto.file.filename}")
            logger.info(f"[UPLOAD] Content-Type: {dto.file.content_type}")

            self.intercept_upload_use_case.start_upload(dto, job_id)

            return {'job_id': job_id}, 202

        except Exception as e:
            logger.exception("[UPLOAD] Erro interno ao iniciar o job")
            return {'message': 'Internal Server Error', 'log': f'{e}'}, 500


# Blueprint e registro do controller
blueprint_upload = Blueprint('blueprint_upload', __name__)
api = Api(blueprint_upload)

api.add_resource(
    InterceptacaoUploadController,
    '/interceptacao/upload',
    resource_class_kwargs={'intercept_upload_use_case': UploadInterceptacaoFactory.create()}
)
