from app import db


class ImagenesProductos(db.Model):  # Corregido: faltaba db.Model
    __tablename__ = 'imagenes_productos'

    id_imagen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto', ondelete='CASCADE'), nullable=False)
    nombre_imagen = db.Column(db.String(255), nullable=False)
    ruta_imagen = db.Column(db.String(255), nullable=False)

    # Relaciones
    producto = db.relationship('Producto', back_populates='imagenes')