from marshmallow import Schema, fields, validate




class CategoriaSchema(Schema):
    nombre_categoria = fields.String(required=True, validate=validate.Length(min=3))
    descripcion_categoria = fields.String(required=False, allow_none=True)
    estado = fields.String(required=True, validate=validate.OneOf(['activo', 'eliminado']))




