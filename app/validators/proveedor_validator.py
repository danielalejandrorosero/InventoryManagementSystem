from app.models.proveedores import Proveedor







class ProveedorValidator:


    def validate_create(self, data):


        if 'nombre_proveedor' not in data:
            return {
                'success': False,
                'message': 'El nombre del proveedor es requerido'
            }


        if Proveedor.query.filter_by(nombre_proveedor=data['nombre_proveedor']).first():
            return {
                'success': False,
                'message': 'El nombre del proveedor ya existe'
            }


        if 'email' not in data:
            return {
                'success': False,
                'message': 'El email del proveedor es requerido'
            }


        if Proveedor.query.filter_by(email=data['email']).first():
            return {
                'success': False,
                'message': 'El email del proveedor ya existe'
            }



        if 'telefono' not in data:
            return {
                'success': False,
                'message': 'El telefono del proveedor es requerido'
            }

        if 'contacto' not in data:
            return {
                'success': False,
                'message': 'El contacto del proveedor es requerido'
            }

        if 'direccion' not in data:
            return {
                'success': False,
                'message': 'La direccion del proveedor es requerida'
            }



    def validate_update(self, data):

        if 'nombre_proveedor' not in data:
            return {
                'success': False,
                'message': 'El nombre del proveedor es requerido'
            }

        if Proveedor.query.filter_by(nombre_proveedor=data['nombre_proveedor']).first():
            return {
                'success': False,
                'message': 'El nombre del proveedor ya existe'
            }

        if 'email' not in data:
            return {
                'success': False,
                'message': 'El email del proveedor es requerido'
            }

        if Proveedor.query.filter_by(email=data['email']).first():
            return {
                'success': False,
                'message': 'El email del proveedor ya existe'
            }

        if 'telefono' not in data:
            return {
                'success': False,
                'message': 'El telefono del proveedor es requerido'
            }

        if 'contacto' not in data:
            return {
                'success': False,
                'message': 'El contacto del proveedor es requerido'
            }

        if 'direccion' not in data:
            return {
                'success': False,
                'message': 'La direccion del proveedor es requerida'
            }


    def validate_delete(self,data):

        if 'id' not in data:
            return {
                'success': False,
                'message': 'El id del proveedor es requerido'
            }


        # el proveedor no existe
        if not Proveedor.query.get(data['id']):
            return {
                'success': False,
                'message': 'El proveedor no existe'
            }


        # el proveedor ya esta eliminado
        if Proveedor.query.get(data['id']).estado != 'activo':
            return {
                'success': False,
                'message': 'El proveedor ya esta eliminado'
            }

        return {
            'success': True,
            'message': 'El proveedor se puede eliminar'
        }






































































































