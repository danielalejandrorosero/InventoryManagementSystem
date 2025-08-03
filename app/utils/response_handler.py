from flask import jsonify


class ResponseHandler:

    """ clase para manejar respuestas HTTP  de forma consistente"""


    def success(self, message, status_code=200):

        """ Respuesta exitosa con mensaje y código de estado """

        return jsonify({'msg': message}), status_code

    def success_data(self, data, status_code=200):
        """ Respuesta exitosa con datos y código de estado """
        return jsonify({'data': data}), status_code


    def error(self, message, status_code=400):
        """ Respuesta de error con mensaje y código de estado """
        return jsonify({'msg': message}), status_code


    def server_error(self, message, status_code=500):
        """ Respuesta de error con mensaje y código de estado """
        return jsonify({'msg': message}), status_code