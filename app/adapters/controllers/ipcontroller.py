from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from app.application.usecases.getallipusecase import GetAllIPUseCase
from app.application.factories.ipfactory import IPFactory

class IPController(Resource):
    def __init__(self, **kwargs):
        self.get_all_ip_use_case: GetAllIPUseCase = kwargs['get_all_ip_use_case']
        self.req_parser = reqparse.RequestParser()
    
    def get(self):
        """
        Retorna a lista de IPs por ordem de acesso.
        ---
        tags:
          - IPs
        responses:
          200:
            description: Lista de IPs por ordem de acesso
            schema:
              type: object
              properties:
                IPs:
                  type: String
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: ID do IP
                      internalTicketNumber:
                        type: String
                        description: Internal Ticket Number
                      ip:
                        type: String
                        description: IP
                      versao:
                        type: String
                        description: Versao atual do IP 
                      timestamp:
                        type: TIMESTAMP
                        description: Timestamp do IP
                      data:
                        type: DATE
                        description: Data de acesso ao IP 
                      hora:
                        type: TIME
                        description: Hora de acesso ao IP
          500:
            description: Erro interno do servidor
        """
        try:
            ips = self.get_all_ip_use_case.execute()
            return {'IPs': [ip.to_dict() for ip in ips]}, 200
        except Exception as e:
            print(f'An error occurred: {e}')
            return {'Message': 'Internal Server Error'}, 500

blueprint_ip = Blueprint('blueprint_ip', __name__)
api = Api(blueprint_ip)

api.add_resource(
    IPController,
    '/ip',
    resource_class_kwargs={'get_all_ip_use_case': IPFactory.get_all_IP()}
)
