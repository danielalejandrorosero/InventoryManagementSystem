from marshmallow import Schema, fields, validate
# para al listar tambien vea la foto del producto

class ProductoSchema(Schema):
    id_producto = fields.Integer(required=False)
    nombre_producto = fields.String (required=True, validate=validate.Length(min=3))
    codigo = fields.String(required=True, validate=validate.Length(min=3))
    sku = fields.String(required=True, validate=validate.Length(min=3))
    descripcion = fields.String(required=False, allow_none=True)
    precio_compra = fields.Float(required=True)
    precio_venta = fields.Float(required=True)
    id_unidad_medida = fields.Integer(required=True)
    stock_minimo = fields.Float(required=False, load_default=0.0)
    stock_maximo = fields.Float(required=False, load_default=0.0)
    id_categoria = fields.Integer(required=False, allow_none=True)
    fecha_creacion = fields.DateTime(required=False)
    fecha_actualizacion = fields.DateTime(required=False)
    id_proveedor = fields.Integer(required=False, allow_none=True)
    estado = fields.String(required=True, validate=validate.OneOf(['activo', 'eliminado']))


class ImagenProductoSchema(Schema):
    id_imagen = fields.Int()
    nombre_imagen = fields.Str()
    ruta_imagen = fields.Str()


class ListarProductosSchema(Schema):
    id_producto = fields.Integer()
    nombre_producto = fields.String()
    codigo = fields.String()
    sku = fields.String()
    #descripcion = fields.String(allow_none=True)
    precio_compra = fields.Float()
    precio_venta = fields.Float()
    #id_unidad_medida = fields.Integer()
    stock_minimo = fields.Float()
    stock_maximo = fields.Float()
    id_categoria = fields.Integer(allow_none=True)
    #fecha_creacion = fields.DateTime()
    #fecha_actualizacion = fields.DateTime()
    id_proveedor = fields.Integer(allow_none=True)

    # Imagen asociada al producto (puede ser None si no tiene imagen)
    imagen = fields.Nested(ImagenProductoSchema, allow_none=True)


class BuscarProductosSchema(Schema):
    id_producto = fields.Integer()
    nombre_producto = fields.String()
    codigo = fields.String()
    sku = fields.String()
    descripcion = fields.String(allow_none=True)
    precio_compra = fields.Float()
    precio_venta = fields.Float()
    id_unidad_medida = fields.Integer()
    stock_minimo = fields.Float()
    stock_maximo = fields.Float()
    id_categoria = fields.Integer(allow_none=True)
    fecha_creacion = fields.DateTime()
    fecha_actualizacion = fields.DateTime()
    id_proveedor = fields.Integer(allow_none=True)
    estado = fields.String()
    imagen = fields.Nested(ImagenProductoSchema, allow_none=True)
