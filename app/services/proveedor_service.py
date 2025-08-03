from  app.models.proveedores import Proveedor

from app.schemas.proveedores_schemas import ProveedoresSchema
from app.validators.proveedor_validator import ProveedorValidator
from app.database import db
class ProveedorService:


    def __init__(self):
        self.schema = ProveedoresSchema()
        self.validator = ProveedorValidator()



    def crear_proveedor(self, data):

        try:

            validated_data = self.schema.load(data)


            # validaciones

            validated_result = self.validator.validate_create(validated_data)
            if not validated_result['success']:
                return {
                    'success': False,
                    'message': validated_result['message'],
                    'status_code': 400
                }


            nuevo_proveedor = Proveedor(
                contacto=validated_data['contacto'],
                direccion=validated_data['direccion'],
                email=validated_data['email'],
                nombre_proveedor=validated_data['nombre_proveedor'],
                telefono=validated_data['telefono'],
            )


            db.session.add(nuevo_proveedor)
            db.session.commit()

            return {
                'success': True,
                'message': 'Proveedor creado correctamente',
                'status_code': 201,
                'data': self.schema.dump(nuevo_proveedor)
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def editar_proveedor(self, id, data):

        try:
            proveedor = Proveedor.query.get(id)


            if not proveedor or proveedor.estado == 'eliminado':
                return {
                    'success': False,
                    'message': 'Proveedor no encontrado',
                    'status_code': 404
                }

            validated_data = self.schema.load(data)


            validation_result = self.validator.validate_update(proveedor, validated_data)

            if not validation_result('is_valid'):
                return {
                    'success': False,
                    'message': validation_result['message'],
                    'status_code': 400
                }

            self._update_proveedor_fields(proveedor, validated_data)

            db.session.commit()

            return {
                'success': True,
                'message': 'Proveedor actualizado correctamente'
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def _update_proveedor_fields(self, proveedor, data):
            proveedor.contacto = data['contacto']
            proveedor.direccion = data['direccion']
            proveedor.email = data['email']
            proveedor.nombre_proveedor = data['nombre_proveedor']
            proveedor.telefono = data['telefono']


    def eliminar_proveedor(self, id):
        try:

            proveedor = Proveedor.query.get(id)


            if not proveedor or proveedor.estado == 'eliminado':
                return {
                    'success': False,
                    'message': 'Proveedor no encontrado',
                    'status_code': 404
                }

            proveedor.estado = 'eliminado'


            db.session.commit()


            return {
                'success': True,
                'message': 'Proveedor eliminado correctamente'
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }


    def listar_proveedor(self):

        try:
            proveedores = Proveedor.query.filter(Proveedor.estado == 'activo').all()



            if not proveedores:
                return {
                    'success': False,
                    'message': 'No se encontraron proveedores',
                    'status_code': 404
                }

            if proveedores:
                data = self.schema.dump(proveedores)
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





