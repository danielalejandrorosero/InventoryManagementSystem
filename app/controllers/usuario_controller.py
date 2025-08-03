from flask import Blueprint, request, jsonify

from app.services.usuario_service import UsuarioService
from app.utils.response_handler import ResponseHandler




class UsuarioController:
    def __init__(self):
        self.service = UsuarioService()
        self.response_handler = ResponseHandler()




    def registrar_usuario(self):


        try:
            data = request.get_json()

            if not data:
                return self.response_handler.error('No se recibieron datos válidos', 400)


            usuario = self.service.create_usuario(data) # el data es para obtener los datos del usuario que viene del get_json()



            if usuario:
                return self.response_handler.success(usuario, 201)
            else:
                return self.response_handler.error('Error al crear el usuario', 500)


        except Exception as e:
            return self.response_handler.server_error(str(e))



    def editar_usuario(self,id):


        try:
            data = request.get_json()

            if not data:
                return self.response_handler.error('No se recibieron datos válidos', 400)

            usuario = self.service.editar_usuario(id, data)


            if usuario:
                return self.response_handler.success(usuario, 200)
            else:
                return self.response_handler.error('Error al editar el usuario', 500)


        except Exception as e:
            return self.response_handler.server_error(str(e))



    def eliminar_usuario(self,id):
        try:
            usuario = self.service.eliminar_usuario(id)

            if usuario:
                return self.response_handler.success(usuario, 200)
            else:
                return self.response_handler.error('Error al eliminar el usuario', 500)

        except Exception as e:
            return self.response_handler.server_error(str(e))



    def listar_usuarios(self):
        try:
            usuarios = self.service.listar_usuarios()

            if usuarios:
                return self.response_handler.success(usuarios, 200)
            else:
                return self.response_handler.error('Error al listar los usuarios', 500)

        except Exception as e:
            return self.response_handler.server_error(str(e))
