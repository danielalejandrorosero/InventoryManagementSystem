from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.decorators import requiere_nivel
from app.database import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.usuarios_schemas import RegistroSchema, EditarSchema,ListarUsuariosSchema

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/registro', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def registro_usuario():
    try:
        #data = request.get_json()

        data = RegistroSchema().load(request.json)
        if not data:
            return jsonify({'msg': 'No se recibieron datos válidos'}), 400
        
        if isinstance(data, list):
            return jsonify({'msg': 'No se acepta un array, solo un objeto JSON'}), 400

        nombre = data.get('nombre')
        nombre_usuario = data.get('nombreUsuario')
        email = data.get('email')
        password = data.get('password')
        nivel_usuario = data.get('nivel_usuario')

        # Validaciones básicas
        if not all([nombre, nombre_usuario, email, password, nivel_usuario]):
            return jsonify({'msg': 'Faltan datos obligatorios'}), 400

        if not isinstance(password, str) or not password.strip():
            return jsonify({'msg': 'La contraseña no puede estar vacía ni ser inválida'}), 400

        # Validar existencia previa
        if Usuario.query.filter_by(nombreUsuario=nombre_usuario).first():
            return jsonify({'msg': 'El nombre de usuario ya existe'}), 400

        if Usuario.query.filter_by(email=email).first():
            return jsonify({'msg': 'El email ya está registrado'}), 400

        # Generar hash seguro de la contraseña
        password_hash = generate_password_hash(password)
        
        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            nombreUsuario=nombre_usuario,
            email=email,
            password=password_hash,
            nivel_usuario=nivel_usuario
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({'msg': 'Usuario registrado correctamente'}), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'Error interno del servidor: {str(e)}'}), 500

# editar_usuario
@usuarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@requiere_nivel([1, 2])
def editar_usuario(id):

    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'msg': 'Usuario no encontrado'}), 404


    try:
        data = EditarSchema().load(request.json)

    except Exception as err:
        return jsonify({'msg': 'Datos invaldos', 'errors': err.messages}), 400


    # actualizar los datos del usuario

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.nombreUsuario = data.get('nombreUsuario', usuario.nombreUsuario)
    usuario.email = data.get('email', usuario.email)

    # esos 3 datos son los que vamos a usar en el schema de editar

    if 'password' in data:
        usuario.password = generate_password_hash(data['password'])


    if 'nivel_usuario' in data:
        usuario.nivel_usuario = data['nivel_usuario']


    try:
        db.session.commit()
        return jsonify({'msg': 'Usuario actualizado correctamente'}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({'msg': 'Error interno del servidor', 'errors': str(err)}), 500


#listar_usuarios
@usuarios_bp.route('/listar_usuarios', methods=['POST'])
@jwt_required()
@requiere_nivel([1, 2])
def listar_usuarios():
    # Obtener todos los
    usuarios = Usuario.query.all()

    if not usuarios:
        return jsonify({'msg': 'No hay usuarios registrados'}), 404

    try:
        data = ListarUsuariosSchema(many=True).dump(usuarios)

        return jsonify(data), 200

    except Exception as err:
        return jsonify({'msg': 'Error al listar usuarios', 'errors': str(err)}), 500

# eliminar usuario
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@requiere_nivel([1])
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)


    if not usuario:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'msg': 'Usuario eliminado correctamente'}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({'msg': 'Error interno del servidor', 'errors': str(err)}), 500