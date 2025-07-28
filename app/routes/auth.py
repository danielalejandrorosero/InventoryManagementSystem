from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app.models.usuario import Usuario
from app.database import db
from werkzeug.security import check_password_hash
from datetime import datetime
from app.utils.email_utils import enviar_email_recuperacion
from app.schemas.auth_schemas import LoginSchema, RecuperarSchema, RestablecerSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
blacklist = set()


@auth_bp.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        data = schema.load(request.json)
    except Exception as err:
        return jsonify({'msg': 'Datos inválidos', 'errors': err.messages}), 400

    nombre_usuario = data['nombreUsuario']
    password = data['password']

    usuario = Usuario.query.filter_by(nombreUsuario=nombre_usuario).first()
    if usuario and check_password_hash(usuario.password, password):
        token = create_access_token(identity=str(usuario.id_usuario))
        return jsonify(access_token=token), 200

    return jsonify({'msg': 'Credenciales inválidas'}), 401


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({'msg': 'Token revocado correctamente'}), 200


@auth_bp.route('/recuperar', methods=['POST'])
def solicitar_recuperacion():
    schema = RecuperarSchema()
    try:
        data = schema.load(request.json)
    except Exception as err:
        return jsonify({'msg': 'Datos inválidos', 'errors': err.messages}), 400

    email = data['email']
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({'msg': 'Correo no encontrado'}), 400

    token = usuario.generar_token_recuperacion()
    db.session.commit()
    enviar_email_recuperacion(email, token)

    return jsonify({'msg': 'Correo enviado con el token de recuperación'}), 200


@auth_bp.route('/restablecer', methods=['POST'])
def restablecer_contraseña():
    schema = RestablecerSchema()
    try:
        data = schema.load(request.json)
    except Exception as err:
        return jsonify({'msg': 'Datos inválidos', 'errors': err.messages}), 400

    token = data['token']
    password_nuevo = data['nueva_password']

    usuario = Usuario.query.filter_by(token_recuperacion=token).first()
    if not usuario:
        return jsonify({'msg': 'Token de recuperación inválido'}), 400

    if usuario.expira_token < datetime.utcnow():
        return jsonify({'msg': 'Token de recuperación expirado'}), 400

    usuario.restablecer_password(password_nuevo)
    db.session.commit()

    return jsonify({'msg': 'Contraseña restablecida'}), 200
