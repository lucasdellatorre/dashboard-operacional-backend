from flask import Blueprint, request
from flask_restful import Api, Resource
from app.application.usecases.getalltargetnumbersusecase import GetAllTargetNumbersUseCase
from app.application.factories.listaalvossimplesfactory import ListaAlvosSimplesFactory
import time

class AlvoController(Resource):
    def __init__(self, **kwargs):
        self.get_all_alvos: GetAllTargetNumbersUseCase = kwargs['get_all_alvos']

    def get(self):
        """
        Retorna todos os números marcados como alvo.
        Se showSuspects=true, substitui o número pelo apelido do suspeito (se houver) e lista os números vinculados.
        ---
        tags:
          - Alvos
        parameters:
          - name: showSuspects
            in: query
            required: false
            schema:
              type: boolean
            default: false
            description: Se verdadeiro, usa o apelido do suspeito e os números relacionados a ele.
        responses:
          200:
            description: Lista de alvos.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      value:
                        type: string
                      suspect:
                        type: boolean
                      numeros:
                        type: array
                        items:
                          type: string
          500:
            description: Erro interno no servidor
        """
        start_time = time.time()
        try:
            show_suspects = request.args.get("showSuspects", "false").lower() in ("true", "1")
            alvos = self.get_all_alvos.execute(show_suspects)
            response = [a.to_dict() for a in alvos]
            return response, 200
  
        except Exception as e:
            print(f'[ERRO /alvos]: {e}')
            return {'message': 'Erro interno no servidor.'}, 500

        finally:
            duration_ms = (time.time() - start_time) * 1000
            print(f'[INFO /alvos] Tempo de execução: {duration_ms:.2f} ms')

# Blueprint e rota
blueprint_alvo = Blueprint('blueprint_alvo', __name__)
api = Api(blueprint_alvo)

api.add_resource(
    AlvoController,
    '/alvos',
    resource_class_kwargs={
        'get_all_alvos': ListaAlvosSimplesFactory.listar()
    }
)