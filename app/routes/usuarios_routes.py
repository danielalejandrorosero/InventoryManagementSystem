from flask import Blueprint, request, jsonify
from app.decorators import requiere_nivel
from flask_jwt_extended import jwt_required

from app.controllers.usuario_controller import UsuarioController



usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')
controller = UsuarioController()

@usuarios_bp.route('/registro', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def registro_usuario():
    return controller.registrar_usuario()


@usuarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])
def editar_usuario(id):
    return controller.editar_usuario(id)


#listar_usuarios
@usuarios_bp.route('/listar_usuarios', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_usuarios():
    return controller.listar_usuarios()

# eliminar usuario
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@requiere_nivel([1])
def eliminar_usuario(id):
    return controller.eliminar_usuario(id)
