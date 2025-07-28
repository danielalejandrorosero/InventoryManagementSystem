from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import os
from werkzeug.utils import secure_filename
from app.models.imagenes_productos import ImagenesProductos
from app import db

imagenes_productos_bp = Blueprint('imagenes_productos', __name__, url_prefix='/imagenes_productos')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@imagenes_productos_bp.route('/subir_imagen_producto', methods=['POST'])
@jwt_required()
def subir_imagen_producto():
    if 'imagen' not in request.files:
        return jsonify({'msg': 'No se envió ningún archivo'}), 400
    if 'id_producto' not in request.form:
        return jsonify({'msg': 'Falta el id del producto'}), 400
    file = request.files['imagen']
    id_producto = request.form['id_producto']
    if file.filename == '':
        return jsonify({'msg': 'Nombre de archivo vacío'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Renombrar archivo para evitar colisiones
        filename = f"producto_{id_producto}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        # Guardar en la base de datos
        ruta_relativa = f'static/uploads/{filename}'
        imagen = ImagenesProductos(
            id_producto=id_producto,
            nombre_imagen=filename,
            ruta_imagen=ruta_relativa
        )
        try:
            db.session.add(imagen)
            db.session.commit()
            return jsonify({'msg': 'Imagen subida correctamente', 'filename': filename, 'ruta': ruta_relativa}), 201
        except Exception as err:
            db.session.rollback()
            return jsonify({'msg': 'Error al guardar en la base de datos', 'errors': str(err)}), 500
    else:
        return jsonify({'msg': 'Tipo de archivo no permitido'}), 400

