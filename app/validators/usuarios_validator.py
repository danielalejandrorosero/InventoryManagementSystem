from app.models.usuario import Usuario




class UsuarioValidator:

    def validate_create(self, data):



        if data['nombreUsuario'] == '':
            return {
                'is_valid': False,
                'message': 'El nombre de usuario no puede estar vacío'
            }


        if data['email'] == '':
            return {
                'is_valid': False,
                'message': 'El email no puede estar vacío'
            }


        # si el email ya existe y
        if Usuario.query.filter_by(email=data['email']).first():
            return {
                'is_valid': False,
                'message': 'El email ya está registrado'
            }


        # si el nombre de usuario ya existe

        if Usuario.query.filter_by(nombreUsuario=data['nombreUsuario']).first():
            return {
                'is_valid': False,
                'message': 'El nombre de usuario ya está registrado'
            }


        # si el email no tiene un formato válido

        if '@' not in data['email'] or '.' not in data['email']:
            return {
                'is_valid': False,
                'message': 'El email no tiene un formato válido'
            }


        # si el password no tiene al menos 8 caracteres

        if len(data['password']) < 8:
            return {
                'is_valid': False,
                'message': 'El password debe tener al menos 8 caracteres'
            }



        return {
            'is_valid': True,
            'message': 'El usuario es válido'
        }

    def validate_update(self, data, usuario_existente):
        # Validar email si está presente
        if 'email' in data:
            if not data['email'] or '@' not in data['email']:
                return {
                    'is_valid': False,
                    'message': 'Email inválido'
                }

        # Validar nombreUsuario si está presente
        if 'nombreUsuario' in data:
            if not data['nombreUsuario'] or len(data['nombreUsuario']) < 8:
                return {
                    'is_valid': False,
                    'message': 'El nombre de usuario debe tener al menos 8 caracteres'
                }

        # Validar nombre si está presente
        if 'nombre' in data:
            if not data['nombre'] or len(data['nombre']) < 3:
                return {
                    'is_valid': False,
                    'message': 'El nombre debe tener al menos 3 caracteres'
                }

        # Validar password solo si está presente
        if 'password' in data:
            if len(data['password']) < 6:
                return {
                    'is_valid': False,
                    'message': 'El password debe tener al menos 6 caracteres'
                }

        return {'is_valid': True}
