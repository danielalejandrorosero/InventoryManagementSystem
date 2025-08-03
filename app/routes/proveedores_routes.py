from flask import Blueprint, request, jsonify
from app.decorators import requiere_nivel
from flask_jwt_extended import jwt_required
from app.models.proveedores import Proveedor
from app.database import db
from app.schemas.proveedores_schemas import ProveedoresSchema

proveedores_bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

@proveedores_bp.route('/crearProveedor', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def crear_proveedor():
    try:
        data = ProveedoresSchema().load(request.json)
        proveedor = Proveedor(
            nombre_proveedor=data['nombre_proveedor'],
            email=data['email'],
            telefono=data['telefono'],
            contacto=data['contacto'],
            direccion=data['direccion'],
        )
        db.session.add(proveedor)
        db.session.commit()
        return jsonify({'msg': 'Proveedor creado correctamente', 'id_proveedor': proveedor.id_proveedor}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'msg': 'Error al crear el proveedor', 'error': str(e)}), 500

@proveedores_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])
def editar_proveedor(id):
    proveedor = Proveedor.query.get(id)
    if not proveedor or proveedor.estado != 'activo':
        return jsonify({'msg': 'El proveedor no existe'}), 404
    try:
        data = ProveedoresSchema().load(request.json)
        proveedor.nombre_proveedor = data.get('nombre_proveedor', proveedor.nombre_proveedor)
        proveedor.email = data.get('email', proveedor.email)
        proveedor.telefono = data.get('telefono', proveedor.telefono)
        proveedor.contacto = data.get('contacto', proveedor.contacto)
        proveedor.direccion = data.get('direccion', proveedor.direccion)
        db.session.commit()
        return jsonify({'msg': 'Proveedor actualizado correctamente'}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({'msg': 'Error al actualizar el proveedor', 'error': str(err)}), 500


@proveedores_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@requiere_nivel([1, 2])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get(id)
    if not proveedor or proveedor.estado != 'activo':
        return jsonify({'msg': 'El proveedor no existe'}), 404

    try:
        proveedor.estado = 'eliminado'
        db.session.commit()
        return jsonify({'msg': 'Proveedor eliminado correctamente'}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({'msg': 'Error al eliminar el proveedor', 'error': str(err)}), 500

@proveedores_bp.route('/listarProveedores', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_proveedores():
    proveedores = Proveedor.query.filter_by(estado='activo').all()
    if not proveedores:
        return jsonify({'msg': 'No se encontraron proveedores'}), 404
    data = ProveedoresSchema(many=True).dump(proveedores)
    return jsonify({'msg': 'Lista de proveedores activos', 'data': data}), 200
