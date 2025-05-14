import werkzeug
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.dto.interceptacaouploaddto import InterceptacaoUploadDTO
from app.application.factories.uploadfactory import UploadInterceptacaoFactory
from app.application.usecases.interceptacaouploadusecase import InterceptacaoUploadUseCase
from app.infraestructure.utils.logger import logger

class InterceptacaoUploadController(Resource):
    def __init__(self, **kwargs):
        self.intercept_upload_use_case: InterceptacaoUploadUseCase = kwargs['intercept_upload_use_case']
        self.req_parser = reqparse.RequestParser()

    def post(self):
        """
        Faz o upload de um arquivo de interceptação.
        ---
        tags:
          - Interceptação
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: operacaoId
            type: string
            required: true
            description: ID da operação
          - in: formData
            name: file
            type: file
            required: true
            description: Arquivo de interceptação para upload
        responses:
          201:
            description: Upload realizado com sucesso
          400:
            description: Erro de validação nos parâmetros fornecidos
          500:
            description: Erro interno do servidor
        """
        self.req_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        self.req_parser.add_argument('operacaoId', location='form')
        args = self.req_parser.parse_args()
        try:
            intercept_upload_dto = InterceptacaoUploadDTO(**args)
            self.intercept_upload_use_case.execute(intercept_upload_dto)
            return {'Message': 'success'}, 201
        except ValueError as e:
            return {'Message': f'{e}'}, 400
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500

blueprint_upload = Blueprint('blueprint_upload', __name__)
api = Api(blueprint_upload)

api.add_resource(
    InterceptacaoUploadController,
    '/interceptacao/upload',
    resource_class_kwargs={'intercept_upload_use_case': UploadInterceptacaoFactory.create()}
)