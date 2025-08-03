from flask import Blueprint, request, jsonify

from app.services.categoria_service import CategoriaService

from app.utils.response_handler import ResponseHandler



class CategoriaController:

    def __init__(self):
        self.service = CategoriaService()
        self.response_handler = ResponseHandler()




    def crear_categoria(self):

        try:
            data = request.get_json()


            if not data:
                return self.response_handler.bad_request('No data provided')


            categoria = self.service.crear_categoria(data)



            if categoria['success']:
                return self.response_handler.success(categoria['message'], categoria['status_code'])
            else:
                return self.response_handler.error(categoria['message'], categoria['status_code'])

        except Exception as e:
            return self.response_handler.server_error(str(e))

    def editar_categoria(self, id):

        try:
            data = request.get_json()

            if not data:
                return self.response_handler.bad_request('No data provided')


            categoria = self.service.editar_categoria(id, data)

            if categoria['success']:
                return self.response_handler.success(categoria['message'], categoria['status_code'])
            else:
                return self.response_handler.error(categoria['message'], categoria['status_code'])


        except Exception as e:
            return self.response_handler.server_error(str(e))


    def listar_categorias(self):

        try:
            categorias = self.service.listar_categorias()

            if categorias['success']:
                return self.response_handler.success(categorias['data'], 200)
            else:
                return self.response_handler.error(categorias['message'], categorias['status_code'])

        except Exception as e:
            return self.response_handler.server_error(str(e))


    def eliminar_categoria(self, id):

        try:
            categoria = self.service.eliminar_categoria(id)

            if categoria['success']:
                return self.response_handler.success(categoria['message'], categoria['status_code'])
            else:
                return self.response_handler.error(categoria['message'], categoria['status_code'])

        except Exception as e:
            return self.response_handler.server_error(str(e))


