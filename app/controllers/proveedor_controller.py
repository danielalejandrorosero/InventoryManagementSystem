from flask import Blueprint, request, jsonify


from app.services.proveedor_service import ProveedorService
from app.utils.response_handler import ResponseHandler




def ProveedorController():

    def __init__(self):
        self.service = ProveedorService()
        self.response_handler = ResponseHandler()



        try:
            data = request.get_json()

            if not data:
                return self.response_handler.error('No se recibieron datos válidos', 400)


            proveedor = self.service.crear_proveedor(data)


            if proveedor['success']:
                return self.response_handler.success(proveedor['message'], proveedor['status_code'])
            else:
                return self.response_handler.error(proveedor['message'], proveedor['status_code'])



        except Exception as e:
            return self.response_handler.server_error(str(e))




    def editar_proveedor(self,id):
        try:
            data = request.get_json()

            if not data:
                return self.response_handler.error('No se recibieron datos válidos', 400)

            proveedor = self.service.editar_proveedor(id, data)

            if proveedor['success']:
                return self.response_handler.success(proveedor['message'], proveedor['status_code'])
            else:
                return self.response_handler.error(proveedor['message'], proveedor['status_code'])

        except Exception as e:
            return self.response_handler.server_error(str(e))



    def eliminar_proveedor(self,id):

        try:
            proveedor = self.service.eliminar_proveedor(id)

            if proveedor['success']:
                return self.response_handler.success(proveedor['message'], proveedor['status_code'])
            else:
                return self.response_handler.error(proveedor['message'], proveedor['status_code'])



        except Exception as e:
            return self.response_handler.server_error(str(e))


    def listar_proveedores(self):
        try:
            proveedores = self.service.listar_proveedor()

            if proveedores['success']:
                return self.response_handler.success_data(proveedores['data'], proveedores['status_code'])
            else:
                return self.response_handler.error(proveedores['message'], proveedores['status_code'])

        except Exception as e:
            return self.response_handler.server_error(str(e))





