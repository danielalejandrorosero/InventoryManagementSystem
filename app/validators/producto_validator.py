from app.models.productos import Producto
from app.models.proveedores import Proveedor
from app.models.unidades_medida import UnidadMedida
from app.models.categorias import Categoria



class ProductoValidator:
    """ Clase para validar las reglas de negocio de los productos. """


    def validate_create(self, data):

        if data['precio_compra'] <= 0 or data['precio_venta'] <= 0:
            return {
                'is_valid': False,
                'message': 'El precio de compra y venta deben ser mayores a 0'
            }


        # validar si la categoria existe

        if not Categoria.query.filter_by(id_categoria=data['id_categoria']).first():
            return {
                'is_valid': False,
                'message': 'La categoría especificada no existe'
            }


        # validar si la unidad de medida existe
        if not UnidadMedida.query.filter_by(id_unidad=data['id_unidad_medida']).first():
            return {
                'is_valid': False,
                'message': 'La unidad de medida especificada no existe'
            }


        # validar si el proveedor existe

        if not Proveedor.query.filter_by(id_proveedor=data['id_proveedor']).first():
            return {
                'is_valid': False,
                'message': 'El proveedor especificado no existe'
            }

        # Validar código único
        if Producto.query.filter_by(codigo=data['codigo']).first():
            return {
                'is_valid': False,
                'message': 'El código del producto ya existe'
            }

        # Validar SKU único
        if Producto.query.filter_by(sku=data['sku']).first():
            return {
                'is_valid': False,
                'message': 'El SKU del producto ya existe'
            }

        return {'is_valid': True}

    def validate_update(self, data, producto):

        # Validar precios
        if data['precio_compra'] <= 0 or data['precio_venta'] <= 0:
            return {
                'is_valid': False,
                'message': 'El precio de compra y venta deben ser mayores a 0'
            }

        # Validar categoría existe
        if not Categoria.query.filter_by(id_categoria=data['id_categoria']).first():
            return {
                'is_valid': False,
                'message': 'La categoría no existe'
            }

        # Validar proveedor existe
        if not Proveedor.query.filter_by(id_proveedor=data['id_proveedor']).first():
            return {
                'is_valid': False,
                'message': 'El proveedor no existe'
            }

        # Validar unidad de medida existe
        if not UnidadMedida.query.filter_by(id_unidad=data['id_unidad_medida']).first():
            return {
                'is_valid': False,
                'message': 'La unidad de medida no existe'
            }

        # Validar código único solo si cambió
        if (data['codigo'] != producto.codigo and
                Producto.query.filter_by(codigo=data['codigo']).first()):
            return {
                'is_valid': False,
                'message': 'El código del producto ya existe'
            }

        # Validar SKU único solo si cambió
        if (data['sku'] != producto.sku and
                Producto.query.filter_by(sku=data['sku']).first()):
            return {
                'is_valid': False,
                'message': 'El SKU del producto ya existe'
            }

        return {'is_valid': True}
