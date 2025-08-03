from flask import Blueprint, request, jsonify

from app.services.producto_service import ProductoService
from app.utils.response_handler import ResponseHandler




class ProductoController:
    def __init__(self):

        self.service = ProductoService()
        self.response_handler = ResponseHandler()


    def crear_producto(self):


        try:
            data = request.get_json()
            if not data:
                return self.response_handler.error('No se recibieron datos válidos', 400)

            producto = self.service.crear_producto(data)

            if producto:
                return self.response_handler.success(producto, 201)
            else:
                return self.response_handler.error('Error al crear el producto', 500)

        except Exception as e:
            return self.response_handler.server_error(str(e))


    def listar_productos(self):
        try:
            productos = self.service.listar_producto()
            if productos['success']:
                return self.response_handler.success_data(productos['data'], 200)

            else:
                return self.response_handler.error(productos['message'], 404)


        except Exception as e:
            return self.response_handler.server_error(str(e))


    def editar_producto(self,id):
        try:
            data = request.get_json()

            if not data:
                return self.response_handler.error('No se recibieron datos válidos', 400)


            producto = self.service.editar_producto(id, data)

            if producto:
                return self.response_handler.success(producto, 200)
            else:
                return self.response_handler.error('Error al editar el producto', 500)


        except Exception as e:
            return self.response_handler.server_error(str(e))




    def eliminar_producto(self, id):
        try:
            producto = self.service.eliminar_producto(id)

            if producto:
                return self.response_handler.success('Producto eliminado correctamente', 200)
            else:
                return self.response_handler.error('Error al eliminar el producto', 500)

        except Exception as e:
            return self.response_handler.server_error(str(e))



    def restaurar_producto(self,id):

        try:
            producto = self.service.restaurar_producto(id)


            if producto:
                return self.response_handler.success('Producto restaurado correctamente', 200)

            else:
                return self.response_handler.error('Error al restaurar el producto', 500)

        except Exception as e:
            return self.response_handler.server_error(str(e))

    def buscar_productos(self):
        """Buscar productos por cualquier campo"""
        try:
            data = request.get_json()
            busqueda = data.get('busqueda', '').strip() if data else ''

            if not busqueda:
                return self.response_handler.error('Debes enviar un valor en "busqueda"', 400)

            resultado = self.service.buscar_productos(busqueda)
            if resultado['success']:
                return self.response_handler.success_data(resultado['data'], 200)
            else:
                return self.response_handler.error(resultado['message'], resultado['status_code'])

        except Exception as e:
            return self.response_handler.server_error(str(e))


    def listar_productos_eliminados(self):
        """Listar productos eliminados"""
        try:
            resultado = self.service.listar_producto_eliminados()
            if resultado['success']:
                return self.response_handler.success_data(resultado['data'], 200)
            else:
                return self.response_handler.error(resultado['message'], resultado['status_code'])

        except Exception as e:
            return self.response_handler.server_error(str(e))
