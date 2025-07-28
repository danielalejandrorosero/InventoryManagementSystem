from marshmallow import Schema, fields, validate

class RegistroSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=3))
    nombreUsuario = fields.String(required=True, validate=validate.Length(min=8))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    nivel_usuario = fields.Integer(required=True)



class EditarSchema(Schema):
    nombre = fields.String(required=False, validate=validate.Length(min=3))
    nombreUsuario = fields.String(required=False, validate=validate.Length(min=8))
    email = fields.Email(required=False)


class ListarUsuariosSchema(Schema):
    id_usuario = fields.Integer()
    nombre = fields.String()
    nombreUsuario = fields.String()
    email = fields.Email()
    nivel_usuario = fields.Integer()