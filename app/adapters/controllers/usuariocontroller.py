from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.factories.userfactory import UserFactory
from app.application.usecases.createuserusecase import CreateUserUseCase
from app.application.dto.usuariodto import UsuarioDTO

class UserController(Resource):
    def __init__(self, **kwargs):
        self.create_usuario_use_case: CreateUserUseCase = kwargs['create_usuario_use_case']
        self.req_parser = reqparse.RequestParser()

    def post(self):
        """
        Cria um novo usuário com base no CPF fornecido.
        ---
        tags:
          - Usuário
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                cpf:
                  type: string
                  description: CPF do usuário a ser criado
        responses:
          201:
            description: Usuário criado com sucesso
            schema:
              type: object
              properties:
                User:
                  type: object
                  properties:
                    cpf:
                      type: string
                      description: CPF do usuário criado
          500:
            description: Erro interno do servidor
        """
        self.req_parser.add_argument('cpf', required=True, location='json')
        args = self.req_parser.parse_args()
        
        try:
            user_dto = UsuarioDTO(cpf=args['cpf'])
            user = self.create_usuario_use_case.execute(user_dto)
            return { 'User': user.to_dict() }, 201
        except Exception as e:
            print(f'An error occurred: {e}')
            return { 'Message': 'Internal Server Error'}, 500

# Blueprint e API registration
blueprint_usuario = Blueprint('blueprint_usuario', __name__)
api = Api(blueprint_usuario)

api.add_resource(
    UserController,
    '/user',
    resource_class_kwargs={ 'create_usuario_use_case': UserFactory.create_user() }
)