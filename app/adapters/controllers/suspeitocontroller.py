from flask import request, Blueprint
from flask_restful import Api, Resource
from app.application.dto.patchnumerosuspeitodto import PatchNumeroSuspeitoDTO
from app.application.factories.suspeitofactory import SuspeitoFactory
from app.application.factories.numerosuspeitofactory import NumeroSuspeitoFactory
from app.application.dto.createsuspeitodto import CreateSuspeitoDTO
from app.application.usecases.adicionanumerosuspeitousecase import AdicionaNumeroSuspeitoUseCase
from app.application.usecases.atualizarsuspeitousecase import AtualizarSuspeitoUseCase
from app.application.usecases.deletarsuspeitousecase import DeletarSuspeitoUseCase
from app.application.usecases.getsuspeitobyidusecase import GetSuspeitoByIdUseCase
from app.application.usecases.deletenumerosuspeitousecase import DeleteNumeroSuspeitoUseCase
from app.application.usecases.createsuspeitousecase import CreateSuspeitoUseCase
from app.application.dto.suspeitoupdatedto import SuspeitoUpdateDTO

class SuspeitoController(Resource):
    def __init__(self, **kwargs):
      self.atualizar_suspeito: AtualizarSuspeitoUseCase = kwargs["atualizar_suspeito"]
      self.deletar_suspeito: DeletarSuspeitoUseCase = kwargs["deletar_suspeito"]
      self.get_suspeito_by_id_use_case: GetSuspeitoByIdUseCase= kwargs["get_suspeito_by_id_use_case"]
        
    def put(self, id):
        """
        Atualiza os dados de um suspeito.
        ---
        tags:
          - Suspeito
        consumes:
          - application/json
        parameters:
          - in: path
            name: id
            required: true
            description: ID do suspeito
            schema:
              type: integer
          - in: header
            name: cpfUsuario
            required: true
            description: CPF do usuário que está realizando a atualização
            schema:
              type: string
              example: "12345678900"
          - in: body
            name: body
            required: true
            description: Campos que podem ser atualizados
            schema:
              type: object
              properties:
                nome:
                  type: string
                cpf:
                  type: string
                apelido:
                  type: string
                anotacoes:
                  type: string
                relevante:
                  type: boolean
        responses:
          200:
            description: Suspeito atualizado com sucesso
          400:
            description: Dados inválidos
          404:
            description: Suspeito não encontrado
          500:
            description: Erro interno
        """
        data = request.get_json(force=True)
        cpf_usuario = request.headers.get("cpfUsuario")
        try:
            dto = SuspeitoUpdateDTO(
              nome=data.get("nome"),
              cpf=data.get("cpf"),
              apelido=data.get("apelido"),
              anotacoes=data.get("anotacoes"),
              relevante=data.get("relevante"),
              lastUpdateCpf=cpf_usuario
          )
            entidade = self.atualizar_suspeito.atualizar_suspeito(id, dto)
            return entidade.to_dict(), 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except LookupError as le:
            print(le)
            return {"error": "Suspeito não encontrado."}, 404
        except Exception as e:
            print(e)
            return {"error": "Erro interno."}, 500

    def delete(self, id):
        """
        Deleta um suspeito pelo ID.
        ---
        tags:
          - Suspeito
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID do suspeito
        responses:
          200:
            description: Suspeito deletado com sucesso
          404:
            description: Suspeito não encontrado
          500:
            description: Erro interno
        """
        try:
            self.deletar_suspeito.execute(id)
            return { "message": "Suspeito deletado com sucesso!" }, 200
        except LookupError:
            return { "message": "Suspeito não encontrado." }, 404
        except Exception as e:
            print(f"[ERROR] {e}")
            return { "message": "Erro interno no servidor." }, 500            
        
    def get(self, id: int):
        """
        Busca os dados detalhados de um suspeito pelo ID.
        ---
        tags:
          - Suspeito
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID do suspeito
        responses:
          200:
            description: Suspeito encontrado com sucesso
          404:
            description: Suspeito não encontrado
          500:
            description: Erro interno
        """
        try:
            suspeito = self.get_suspeito_by_id_use_case.execute(id)
            if not suspeito:
                return {"message": "Suspeito não encontrado"}, 404
            return suspeito.to_dict(), 200
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500
                
class SuspeitoCreateController(Resource):
    def __init__(self, **kwargs):
        self.create_suspeito_use_case: CreateSuspeitoUseCase = kwargs['create_suspeito_use_case']
    def post(self):
        """
        Cria um novo suspeito.
        ---
        tags:
          - Suspeito
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - apelido
                - numeros_ids
              properties:
                apelido:
                  type: string
                nome:
                  type: string
                cpf:
                  type: string
                numeros_ids:
                  type: array
                  items:
                    type: integer
          - name: cpfUsuario
            in: header
            required: true
            schema:
              type: string
              example: "12345678900"
        responses:
          201:
            description: Suspeito criado com sucesso
          400:
            description: Erro de validação
          500:
            description: Erro interno
        """
        data = request.get_json()
        cpf_usuario = request.headers.get("cpfUsuario")

        if not cpf_usuario:
            return {"message": "Cabeçalho 'cpfUsuario' é obrigatório."}, 400

        try:
            dto = CreateSuspeitoDTO.from_dict(data)
            dto.lastUpdateCpf = cpf_usuario
            result = self.create_suspeito_use_case.execute(dto)
            return result.to_dict(), 201
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500


class SuspeitoDetailController(Resource):
    def __init__(self, **kwargs):
        self.get_suspeito_by_id_use_case: GetSuspeitoByIdUseCase = kwargs['get_suspeito_by_id_use_case']
    def get(self, id: int):
        """
        Busca os dados detalhados de um suspeito pelo ID.
        ---
        tags:
          - Suspeito
        parameters:
          - in: path
            name: id
            required: true
            schema:
              type: integer
            description: ID do suspeito
        responses:
          200:
            description: Suspeito encontrado com sucesso
          404:
            description: Suspeito não encontrado
          500:
            description: Erro interno
        """
        try:
            suspeito = self.get_suspeito_by_id_use_case.execute(id)
            if not suspeito:
                return {"message": "Suspeito não encontrado"}, 404
            return suspeito.to_dict(), 200
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500
        
class ManageNumeroController(Resource):
    def __init__(self, **kwargs):
        self.delete_numero_use_case: DeleteNumeroSuspeitoUseCase = kwargs['delete_numero_use_case']

    def delete(self, id: int, numeroId: int):
        """
        Remove a associação de um número com um suspeito.
        ---
        tags:
          - Suspeito
        parameters:
          - in: path
            name: id
            required: true
            description: ID do suspeito
            schema:
              type: integer
          - in: path
            name: numeroId
            required: true
            description: ID do número
            schema:
              type: integer
        responses:
          200:
            description: Associação removida com sucesso
          400:
            description: Não é permitido remover o único número vinculado ao suspeito.
          500:
            description: Erro interno
        """
        try:
            cpf_usuario = request.headers.get("cpfUsuario")
            is_removed = self.delete_numero_use_case.execute(id, numeroId)
            if is_removed:
                return { "message": "Número desvinculado com sucesso." }, 200
            return { "message": "Não é permitido remover o único número vinculado ao suspeito." }, 400
        except Exception as e:
            print(f"[ERROR] {e}")
            return {"message": "Erro interno no servidor"}, 500
          
class AtualizaNumeroController(Resource):
    def __init__(self, **kwargs):
        self.adicionar_numero_suspeito_use_case: AdicionaNumeroSuspeitoUseCase = kwargs['adicionar_numero_suspeito_use_case']
              
    def post(self, id: int):
        """
        Adiciona uma lista de telefones para um suspeito.
        ---
        tags:
          - Suspeito
        parameters:
          - name: id
            in: path
            required: true
            type: integer
            description: ID do suspeito
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - numerosIds
              properties:
                numerosIds:
                  type: array
                  items:
                    type: integer
                  example: [1, 2, 3]
                  description: Lista de IDs dos telefones a serem vinculados
          - name: cpfUsuario
            in: header
            required: true
            type: string
            example: "12345678900"
            description: CPF do usuário autenticado
        responses:
          200:
            description: Telefones adicionados com sucesso ao suspeito
          404:
            description: Suspeito não encontrado
          500:
            description: Erro interno
        """
        data = request.get_json()
        cpfUsuario = request.headers.get("cpfUsuario")
        try:
            numero_suspeito_dto = PatchNumeroSuspeitoDTO(**data | { 'cpf': cpfUsuario, 'suspeitoId': id })
            result = self.adicionar_numero_suspeito_use_case.execute(numero_suspeito_dto)
            if result:
              return { 'Message:': 'números adicionados com sucesso!' }, 200
            return { 'Message:': 'erro ao adicionar números' }, 400
        except ValueError as ve:
            return {'message': str(ve)}, 404
        except Exception as e:
            print(f'[ERRO PATCH /numeros]: {e}')
            return {'message': 'Erro interno no servidor.'}, 500

# Blueprint e API registration
blueprint_suspeito = Blueprint('blueprint_suspeito', __name__)
api = Api(blueprint_suspeito)

api.add_resource(
    SuspeitoController,
    "/suspeito/<int:id>",
    resource_class_kwargs={
        "atualizar_suspeito": SuspeitoFactory.atualizar_suspeito(),
        "deletar_suspeito": SuspeitoFactory.delete_suspeito(),
        "get_suspeito_by_id_use_case": SuspeitoFactory.get_suspeito_by_id()
    }
)

api.add_resource(
    SuspeitoCreateController,
    "/suspeito",
    resource_class_kwargs={
        "create_suspeito_use_case": SuspeitoFactory.create_suspeito()
    }
)

api.add_resource(
    SuspeitoDetailController,
    "/suspeito/<int:id>",
    resource_class_kwargs={
        "get_suspeito_by_id_use_case": SuspeitoFactory.get_suspeito_by_id()
    }
)

api.add_resource(
    AtualizaNumeroController,
    "/suspeito/<int:id>/numero",
    resource_class_kwargs={
        "adicionar_numero_suspeito_use_case": SuspeitoFactory.adicionar_telefones()
    }
)

api.add_resource(
    ManageNumeroController,
    "/suspeito/<int:id>/numero/<int:numeroId>",
    resource_class_kwargs={
        "delete_numero_use_case": NumeroSuspeitoFactory.delete_number(),
        "adicionar_numero_suspeito_use_case": SuspeitoFactory.adicionar_telefones()
    }
)
