from flask import Blueprint
from flask_restful import Api, Resource
from app.application.factories.testfactory import TestFactory
from app.application.usecases.sayhiusecase import SayHiUseCase

class TestController(Resource):
    def __init__(self, say_hi_use_case: SayHiUseCase):  # Explicit type
        self.say_hi_use_case = say_hi_use_case
    
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.say_hi_use_case = kwargs['say_hi_use_case']
        
    def get(self):
        """
        This examples uses FlaskRESTful Resource
        It works also with swag_from, schemas and spec_dict
        ---
        tags:
          - Test
        parameters:
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        some_value = self.say_hi_use_case.execute()
        return { 'Message': some_value }, 200
    
blueprint_test = Blueprint('blueprint_test', __name__)

api = Api(blueprint_test)
api.add_resource(TestController, '/test', resource_class_kwargs={ 'say_hi_use_case': TestFactory.create_say_hi_use_case()})