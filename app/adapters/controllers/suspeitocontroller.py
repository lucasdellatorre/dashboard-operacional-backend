# from flask import Blueprint, jsonify
# from flask_restful import Api, Resource, reqparse
# from app.application.factories.suspeitofactory import SuspeitoFactory
# from app.application.usecases.createsuspeitousecase import CreateSuspeitoUseCase
# from app.application.dto.alvodto import AlvoDTO
# from app.domain.services.alvoservice import AlvoService

# class SuspeitoController(Resource):
#     def __init__(self, **kwargs):
#         self.create_alvo_use_case: CreateSuspeitoUseCase = kwargs['create_alvo_use_case']
#         self.req_parser = reqparse.RequestParser()

#     def post(self):
#         """
#         Cria um novo alvo com base nas informações fornecidas.
#         ---
#         parameters:
#           - in: body
#             name: body
#             required: true
#             schema:
#               type: object
#               properties:
#                 internalTicketNumber:
#                   type: string
#                   description: Número do ticket interno do alvo
#                 descricao:
#                   type: string
#                   description: Descrição do alvo
#                 nome:
#                   type: string
#                   description: Nome do alvo
#                 cpf:
#                   type: string
#                   description: CPF do alvo
#         responses:
#           201:
#             description: Alvo criado com sucesso
#             schema:
#               type: object
#               properties:
#                 Suspeito:
#                   type: object
#                   properties:
#                     internalTicketNumber:
#                       type: string
#                       description: Número do ticket interno do alvo
#                     descricao:
#                       type: string
#                     nome:
#                       type: string
#                     cpf:
#                       type: string
#           500:
#             description: Erro interno do servidor
#         """
#         self.req_parser.add_argument('internalTicketNumber', required=True, location='json')
#         self.req_parser.add_argument('descricao', required=True, location='json')
#         self.req_parser.add_argument('nome', required=True, location='json')
#         self.req_parser.add_argument('cpf', required=True, location='json')
        
#         args = self.req_parser.parse_args()

#         try:
#             suspeito_dto = AlvoDTO(**args)
#             suspeito = self.create_alvo_use_case.execute(suspeito_dto)
#             return {'Suspeito': suspeito.to_dict()}, 201
#         except Exception as e:
#             print(f'An error occurred: {e}')
#             return {'Message': 'Internal Server Error'}, 500
          
#     def get(self):
#         """
#         Retorna a lista de alvos ordenados por Internal Ticket Number.
#         ---
#         tags:
#           - Alvo
#         responses:
#           200:
#             description: Lista de alvos
#             schema:
#               type: object
#               properties:
#                 Suspeitos:
#                   type: array
#                   items:
#                     type: object
#                     properties:
#                       internalTicketNumber:
#                         type: string
#                         description: Número do ticket interno do alvo
#                       descricao:
#                         type: string
#                       nome:
#                         type: string
#                       cpf:
#                         type: string
#           500:
#             description: Erro interno do servidor
#         """
#         try:
#             alvo_service = AlvoService()
#             alvos = alvo_service.list_alvos()
#             return jsonify({'Suspeitos': [alvo.to_dict() for alvo in alvos]}), 200
#         except Exception as e:
#             print(f'An error occurred: {e}')
#             return jsonify({'Message': 'Internal Server Error'}), 500


# # Blueprint e API registration
# blueprint_alvo = Blueprint('blueprint_alvo', __name__)
# api = Api(blueprint_alvo)

# api.add_resource(
#     SuspeitoController,
#     '/suspeito',
#     resource_class_kwargs={'create_alvo_use_case': SuspeitoFactory.create_suspeito()}
# )
