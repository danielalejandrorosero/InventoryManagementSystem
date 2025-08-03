
from app.models.categorias import Categoria

class CategoriaValidator:

    def validate_create(self,data):

        if not data.get('nombre_categoria'):
            return {
                'is_valid': False,
                'message': 'El nombre de la categoría es obligatorio'
            }



        if Categoria.query.filter_by(nombre_categoria=data['nombre_categoria']).first():
            return {
                'is_valid': False,
                'message': 'El nombre de la categoría ya está registrado'
            }

        if not data.get('descripcion_categoria'):
            return {
                'is_valid': False,
                'message': 'La descripción de la categoría es obligatoria'
            }

        return {'is_valid': True}


    def validate_update(self, data, categoria):
        if not data.get('nombre_categoria'):
            return {
                'is_valid': False,
                'message': 'El nombre de la categoría es obligatorio'
            }

        if not data.get('estado'):
            return {
                'is_valid': False,
                'message': 'El estado de la categoría es obligatorio'
            }

        # Validar si el nombre de la categoría ya existe, excepto para la categoría actual
        if Categoria.query.filter(Categoria.nombre_categoria == data['nombre_categoria'], Categoria.id_categoria != categoria.id_categoria).first():
            return {
                'is_valid': False,
                'message': 'El nombre de la categoría ya está registrado'
            }

        return {'is_valid': True}
    def validate_delete(self, categoria):
        if categoria.productos:
            return {
                'is_valid': False,
                'message': 'No se puede eliminar la categoría porque tiene productos asociados'
            }



        return {'is_valid': True}


    def validate_list(self, data):

        if not data.get('estado'):
            return {
                'is_valid': False,
                'message': 'El estado de la categoría es obligatorio'
            }

        # Validar si el estado es válido
        if data['estado'] not in ['activo', 'inactivo']:
            return {
                'is_valid': False,
                'message': 'El estado debe ser "activo" o "inactivo"'
            }

        return {'is_valid': True}