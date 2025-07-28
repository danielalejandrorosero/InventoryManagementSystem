from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    nombreUsuario = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True)


class RecuperarSchema(Schema):
    email = fields.Email(required=True)



class RestablecerSchema(Schema):
    token = fields.String(required=True)
    nueva_password = fields.Str(required=True, validate=validate.Length(min=3))