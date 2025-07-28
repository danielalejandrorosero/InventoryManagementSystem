from functools import wraps

from flask import request, jsonify

from flask_jwt_extended import jwt_required, get_jwt

from app.models import Usuario, Grupo


def requiere_nivel(niveles_permitidos):
    def decorator(func):

        @wraps(func)

        def wrapper(*args, **kwargs):

            id_usuario = get_jwt()['sub']
            usuario = Usuario.query.get(id_usuario)

            if not usuario:
                return jsonify({'msg': 'Usuario no encontrado'}), 401


            grupo = usuario.grupo


            if not grupo:
                return jsonify({'msg': 'Grupo no encontrado'}), 401
            




            if grupo.nivel_grupo not in niveles_permitidos:
                return jsonify({'msg': 'No tienes permisos para acceder a esta ruta'}), 401
            


            return func(*args, **kwargs)
        
        return wrapper
    return decorator


