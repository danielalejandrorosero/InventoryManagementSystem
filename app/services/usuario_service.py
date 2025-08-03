from app.schemas.usuarios_schemas import ListarUsuariosSchema, RegistroSchema, EditarSchema
from app.validators.usuarios_validator import UsuarioValidator

from app.database import db
from app.models.usuario import Usuario

from werkzeug.security import generate_password_hash


class UsuarioService:

    def __init__(self):
        self.validator = UsuarioValidator()
        self.create_schema = RegistroSchema()
        self.list_schema = ListarUsuariosSchema()
        self.edit_schema = EditarSchema()



    def create_usuario(self,data):

        try:
            validated_data = self.create_schema.load(data)


            validated_result = self.validator.validate_create(validated_data)

            if not validated_result['is_valid']:
                return {
                    'success': False,
                    'message': validated_result['message'],
                    'status_code': 400
                }


            nuevo_usuario = Usuario(
                nombre=validated_data['nombre'],
                nombreUsuario=validated_data['nombreUsuario'],
                email=validated_data['email'],
                password=validated_data['password'],
                nivel_usuario=validated_data['nivel_usuario']
            )

            db.session.add(nuevo_usuario)
            db.session.commit()

            return {
                'success': True,
                'message': 'Usuario creado correctamente',
                'data': nuevo_usuario.id_usuario
            }

        except Exception as e:
            db.session.rollback()

            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def listar_usuarios(self):

        try:
            usuarios  = Usuario.query.all()


            if not usuarios:
                return {
                    'success': False,
                    'message': 'No hay usuarios registrados',
                    'status_code': 404
                }

            data = self.list_schema.dump(usuarios, many=True)

            return {
                'success': True,
                'data': data
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }


    def editar_usuario(self, id, data):

        try:
            usuario = Usuario.query.get(id)

            if not usuario:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado',
                    'status_code': 404
                }

            # validar datos
            validated_data = self.edit_schema.load(data)


            validation_result = self.validator.validate_update(validated_data, usuario)


            if not validation_result['is_valid']:
                return {
                    'success': False,
                    'message': validation_result['message'],
                    'status_code': 400
                }


            # actualizar los datos del usuario

            self._update_usuario(usuario, validated_data)

            db.session.commit()


            return {
                'success': True,
                'message': 'Usuario actualizado correctamente',
                'data': self.list_schema.dump(usuario)
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def eliminar_usuario(self,id):

        try:
            usuario = Usuario.query.get(id)

            if not usuario:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado',
                    'status_code': 404
                }

            db.session.delete(usuario)

            return {
                'success': True,
                'message': 'Usuario eliminado correctamente'
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }


    def _update_usuario(self, usuario, data):
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.nombreUsuario = data.get('nombreUsuario', usuario.nombreUsuario)
        usuario.email = data.get('email', usuario.email)
        # No modificar password aquí
        # No modificar nivel_usuario aquí (solo si lo deseas explícitamente)
