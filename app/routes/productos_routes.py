from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.decorators import requiere_nivel
from app.controllers.producto_controller import ProductoController


productos_bp = Blueprint('productos', __name__, url_prefix='/productos')
controller = ProductoController()





@productos_bp.route('/crearProducto', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def crear_producto():
    return controller.crear_producto()


@productos_bp.route('/listarProductos', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_productos():
    return controller.listar_productos()


@productos_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])
def editar_producto(id):
    return controller.editar_producto(id)


@productos_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@requiere_nivel([1, 2])
def eliminar_producto(id):
    return controller.eliminar_producto(id)


@productos_bp.route('/restaurar/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])
def restaurar_producto(id):
    return controller.restaurar_producto(id)


@productos_bp.route('/listar_eliminados', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_productos_eliminados():
    return controller.listar_productos_eliminados()


@productos_bp.route('/buscarProductos', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def buscar_productos():
    return controller.buscar_productos()