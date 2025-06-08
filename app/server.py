from flask import Flask, jsonify, redirect
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from flasgger import Swagger
from app.infraestructure.utils.enviroment import prefix
from app.infraestructure.database.config import ConfigFactory
from app.infraestructure.database.db import db, migrate
from app.adapters.controllers.testcontroller import blueprint_test
from app.adapters.controllers.usuariocontroller import blueprint_usuario
from app.adapters.controllers.operacaocontroller import blueprint_operacao
from app.adapters.controllers.uploadcontroller import blueprint_upload
from app.adapters.controllers.teiacontroller import blueprint_teia
from app.adapters.controllers.planilhacontroller import blueprint_planilha
from app.adapters.controllers.numerocontroller import blueprint_numero
from app.adapters.controllers.ipcontroller import blueprint_ip
from app.adapters.controllers.suspeitocontroller import blueprint_suspeito
from app.adapters.controllers.suspeitoemailcontroller import blueprint_suspeito_email
from app.adapters.controllers.alvosoperacaocontroller import blueprint_numeros_operacao
from app.adapters.controllers.alvocontroller import blueprint_alvo
from app.adapters.controllers.uploadtrackercontroller import blueprint_progress

def create_app():
    # ============================================
    # Main
    # ============================================

    app = Flask(__name__)
    CORS(app)
    Api(app, prefix=prefix)
    config = ConfigFactory().get_config()
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    
    # ============================================
    # Database
    # ============================================
    
    db.init_app(app)
    migrate.init_app(app, db)
   
    # ============================================
    # Swagger
    # ============================================
    
    Swagger(app)
    
    # ============================================
    # Error Handler
    # ============================================

    @app.errorhandler(NotFound)
    def handle_method_not_found(e):
        response = jsonify({"message": str(e)})
        response.status_code = 404
        return response

    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed_error(e):
        response = jsonify({"message": str(e)})
        response.status_code = 405
        return response

    @app.route('/')
    def redirect_to_prefix():
        if prefix != '':
            return redirect(prefix)

    # ============================================
    # Register blueprint
    # ============================================

    blueprint_list = [
        blueprint_test,
        blueprint_usuario,
        blueprint_operacao,
        blueprint_upload,
        blueprint_teia,
        blueprint_planilha,
        blueprint_numero,
        blueprint_ip,
        blueprint_numeros_operacao, 
        blueprint_suspeito,
        blueprint_alvo,
        blueprint_progress,
        blueprint_suspeito_email
    ]

    for blueprint in blueprint_list:
        app.register_blueprint(blueprint, url_prefix=f'/{prefix}')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)