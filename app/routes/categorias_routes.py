from flask import Blueprint, request, jsonify



from app.decorators import requiere_nivel
from flask_jwt_extended import jwt_required

from app.controllers.categoria_controller import CategoriaController

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

controller = CategoriaController()


@categorias_bp.route('/crearCategoria', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def crear_categoria():
    return controller.crear_categoria()

@categorias_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])
def editar_categoria(id):
    return controller.editar_categoria(id)

# eliminar categoria activo o eliminado
@categorias_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@requiere_nivel([1, 2])
def eliminar_categoria(id):
    return controller.eliminar_categoria(id)


@categorias_bp.route('/listarCategorias', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_categorias():
    return controller.listar_categorias()
