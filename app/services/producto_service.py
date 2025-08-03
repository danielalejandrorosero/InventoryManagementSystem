from app.models.productos import Producto
from app.models.proveedores import Proveedor
from app.models.unidades_medida import UnidadMedida
from app.models.categorias import Categoria
from app.database import db
from app.schemas.productos_schemas import ProductoSchema, ListarProductosSchema
from app.validators.producto_validator import ProductoValidator



class ProductoService:
    def __init__(self):
        self.validator = ProductoValidator()
        self.schema = ProductoSchema()
        self.list_schema = ListarProductosSchema(many=True)

    def crear_producto(self, data):

        try:

            validated_data = self.schema.load(data)

            # validacion del negocio

            validated_result = self.validator.validate_create(validated_data)
            if not validated_result['is_valid']:
                return {
                    'success': False,
                    'message': validated_result['message'],
                    'status_code': 400
                }


            nuevo_producto = Producto(
                nombre_producto=validated_data['nombre_producto'],
                codigo=validated_data['codigo'],
                sku=validated_data['sku'],
                descripcion=validated_data['descripcion'],
                precio_compra=validated_data['precio_compra'],
                precio_venta=validated_data['precio_venta'],
                id_unidad_medida=validated_data['id_unidad_medida'],
                stock_minimo=validated_data.get('stock_minimo', 0.0),
                stock_maximo=validated_data.get('stock_maximo', 0.0),
                id_categoria=validated_data['id_categoria'],
                id_proveedor=validated_data['id_proveedor'],
            )


            db.session.add(nuevo_producto)
            db.session.commit()


            return {
                'success': True,
                'message': 'Producto creado correctamente',
                'data': nuevo_producto.id_producto
            }

        except Exception as e:
            db.session.rollback()

            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }


    def listar_producto(self):

        try:
            productos = Producto.query.filter_by(estado='activo').all()


            if not productos:
                return {
                    'success': False,
                    'message': 'No se encontraron productos',
                    'status_code': 404
                }


            productos_con_imagen = self._format_productos_with_images(productos)
            data = self.list_schema.dump(productos_con_imagen)



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


    def editar_producto(self,id, data):

        try:
            producto = Producto.query.get(id)

            if not producto or producto.estado == 'eliminado':
                return {
                    'success': False,
                    'message': 'Producto no encontrado',
                    'status_code': 404
                }

            # validar datos
            validated_data = self.schema.load(data)

            # validar para edicion
            validation_result = self.validator.validate_update(validated_data, producto)
            if not validation_result['is_valid']:
                return {
                    'success': False,
                    'message': validation_result['message'],
                    'status_code': 400
                }

            self._update_producto_fields(producto, validated_data)

            db.session.commit()
            return {
                'success': True,
                'message': 'Producto actualizado correctamente'
            }


        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }



    def eliminar_producto(self, id):

        try:
            producto = Producto.query.get(id)


            if not producto:
                return {
                    'success': False,
                    'message': 'Producto no encontrado',
                    'status_code': 404
                }

            producto.estado = 'eliminado'

            db.session.commit()

            return {
                'success': True,
                'message': 'Producto eliminado correctamente'
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }



    def restaurar_producto(self, id):

        try:
            producto = Producto.query.get(id)

            if not producto:
                return {
                    'success': False,
                    'message': 'Producto no encontrado',
                    'status_code': 404
                }


            if producto.estado != 'eliminado':
                return {
                    'success': False,
                    'message': 'El producto no está marcado como eliminado',
                    'status_code': 400
                }


            producto.estado = 'activo'
            db.session.commit()

            return {
                'success': True,
                'message': 'Producto restaurado correctamente'
            }

        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def listar_producto_eliminados(self):

        try:
            producto = Producto.query.filter_by(estado='eliminado').all()


            if not producto:
                return {
                    'success': False,
                    'message': 'No se encontraron productos eliminados',
                    'status_code': 404
                }


            productos_con_imagen = self._format_productos_with_images(producto)
            data = self.list_schema.dump(productos_con_imagen)

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


    def buscar_productos(self, busqueda):
        try:
            like = f"%{busqueda}%"
            query = db.session.query(Producto).join(
                Producto.categoria
            ).join(
                Producto.proveedor
            ).join(
                Producto.unidad_medida
            ).filter(
                db.or_(
                    Producto.nombre_producto.ilike(like),
                    Producto.codigo.ilike(like),
                    Producto.sku.ilike(like),
                    Producto.descripcion.ilike(like),
                    Categoria.nombre_categoria.ilike(like),
                    Proveedor.nombre_proveedor.ilike(like),
                    UnidadMedida.nombre.ilike(like)
                ),
                Producto.estado == 'activo'
            )
            productos = query.all()
            # Serializar resultados usando el schema correcto
            from app.schemas.productos_schemas import ListarProductosSchema
            result = ListarProductosSchema(many=True).dump(productos)
            return {
                'success': True,
                'data': result,
                'status_code': 200
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno del servidor: {str(e)}',
                'status_code': 500
            }

    def _format_productos_with_images(self, productos):
        """Método privado para formatear productos con imágenes"""
        productos_con_imagen = []
        for producto in productos:
            imagen = None
            if hasattr(producto, 'imagenes') and producto.imagenes:
                img = producto.imagenes[0]
                imagen = {
                    'id_imagen': img.id_imagen,
                    'nombre_imagen': img.nombre_imagen,
                    'ruta_imagen': img.ruta_imagen
                }

            prod_dict = {
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'codigo': producto.codigo,
                'sku': producto.sku,
                'precio_compra': producto.precio_compra,
                'precio_venta': producto.precio_venta,
                'stock_minimo': producto.stock_minimo,
                'stock_maximo': producto.stock_maximo,
                'id_categoria': producto.id_categoria,
                'id_proveedor': producto.id_proveedor,
                'imagen': imagen
            }
            productos_con_imagen.append(prod_dict)

        return productos_con_imagen


    def _update_producto_fields(self, producto, data):
        """Método privado para actualizar campos del producto"""
        producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
        producto.codigo = data.get('codigo', producto.codigo)
        producto.sku = data.get('sku', producto.sku)
        producto.descripcion = data.get('descripcion', producto.descripcion)
        producto.precio_compra = data.get('precio_compra', producto.precio_compra)
        producto.precio_venta = data.get('precio_venta', producto.precio_venta)
        producto.id_unidad_medida = data.get('id_unidad_medida', producto.id_unidad_medida)
        producto.stock_minimo = data.get('stock_minimo', producto.stock_minimo)
        producto.stock_maximo = data.get('stock_maximo', producto.stock_maximo)
        producto.id_categoria = data.get('id_categoria', producto.id_categoria)
        producto.id_proveedor = data.get('id_proveedor', producto.id_proveedor)
