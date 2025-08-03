from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

from pathlib import Path
import yaml

from .config import config
from .database import db
from app import models

from flask_mail import Mail

# Importa el blueprint y la blacklist
from app.routes.auth import auth_bp, blacklist
from app.routes.usuarios_routes import usuarios_bp
from app.routes.imagenes_usuarios_routes import imagenes_usuarios_bp
from app.routes.imagenes_productos_routes import imagenes_productos_bp
from app.routes.categorias_routes import categorias_bp
from app.routes.productos_routes import productos_bp

from app.routes.proveedores_routes import proveedores_bp


from flasgger import Swagger
jwt = JWTManager()  # Inicializamos el JWTManager globalmente


mail = Mail()
def create_app(config_name=None):
    app = Flask(__name__)
    config_name = config_name or 'default'
    app.config.from_object(config[config_name])


    # ruta del archivo  yaml

    swagger_path = Path(__file__).resolve().parent / 'swagger.yaml'

    with open(swagger_path, 'r') as f:
        swagger_template = yaml.safe_load(f)

    Swagger(app, template=swagger_template)



    # Inicializar extensiones
    db.init_app(app)
    CORS(app)
    jwt.init_app(app)
    Migrate(app, db)
    mail.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(imagenes_usuarios_bp, url_prefix='/imagenes_usuarios')
    app.register_blueprint(imagenes_productos_bp, url_prefix='/imagenes_productos')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')






    # Callback para verificar si el token está revocado
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklist

    return app
