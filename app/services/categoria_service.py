from app.database import db
from app.schemas.categorias_schemas import CategoriaSchema
from app.validators.categoria_validator import CategoriaValidator
from app.models.categorias import Categoria


class CategoriaService:
    def __init__(self):
        self.validator = CategoriaValidator()

        self.schema = CategoriaSchema()



    def crear_categoria(self, data):

        try:

            validated_data = self.schema.load(data)


            # validacion del negocio

            validated_result = self.validator.validate_create(validated_data)

            if not validated_result['is_valid']:
                return  {
                    'success': False,
                    'message': validated_result['message'],
                    'status_code': 400
                }

            nueva_categoria = Categoria(
                nombre_categoria=validated_data['nombre_categoria'],
                descripcion_categoria=validated_data.get('descripcion_categoria'),
                #estado=validated_data['estado']
            )

            db.session.add(nueva_categoria)
            db.session.commit()

            return {
                'success': True,
                'message': 'Categoría creada correctamente',
                'status_code': 201,
            }
        except Exception as e:
            db.session.rollback()

            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def editar_categoria(self,id,data):
        try:
            categoria = Categoria.query.get(id)


            if not categoria or categoria.estado == 'eliminado':
                return {
                    'success': False,
                    'message': 'Categoría no encontrada',
                    'status_code': 404
                }

            # validar datos del esquema
            validated_data = self.schema.load(data)

            # validar para editar
            validated_result = self.validator.validate_update(validated_data, categoria)

            if not validated_result['is_valid']:
                return {
                    'success': False,
                    'message': validated_result['message'],
                    'status_code': 400
                }

            # actualizar los campos de la categoría
            categoria.nombre_cateoria = validated_data['nombre_categoria']
            categoria.descripcion_categoria = validated_data.get('descripcion_categoria')

            db.session.commit()

            return {
                'success': True,
                'message': 'Categoría actualizada correctamente',
                'status_code': 200
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def eliminar_categoria(self,id):

        try:
            categoria = Categoria.query.get(id)

            validated_result = self.validator.validate_delete(categoria)


            if not validated_result['is_valid']:
                return {
                    'success': False,
                    'message': validated_result['message'],
                    'status_code': 400
                }



            categoria.estado = 'eliminado' if categoria.estado == 'activo' else 'activo'

            db.session.commit()


            return {
                'success': True,
                'message': 'Categoría eliminada correctamente',
                'status_code': 200
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }


    def listar_categorias(self):

        try:
            categorias = Categoria.query.filter(Categoria.estado == 'activo').all()

            validated_result = self.validator.validate_list({'estado': 'activo'})


            if not validated_result['is_valid']:
                return {
                    'success': False,
                    'message': validated_result['message'],
                    'status_code': 400
                }


            categorias_data = self.schema.dump(categorias, many=True)
            return {
                'success': True,
                'message': 'Lista de categorías',
                'data': categorias_data,
                'status_code': 200
            }

        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'status_code': 500
            }
