from marshmallow import Schema, fields, validate

class ProveedoresSchema(Schema):
    nombre_proveedor = fields.String(required=True, validate=validate.Length(min=3))
    contacto = fields.String(required=True, validate=validate.Length(min=3))
    telefono = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    direccion = fields.String(required=True, validate=validate.Length(min=3))

