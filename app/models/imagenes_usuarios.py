from app import db

class ImagenesUsuarios(db.Model):
    __tablename__ = 'imagenes_usuarios'

    id_imagen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    nombre_imagen = db.Column(db.String(255), nullable=False)
    ruta_imagen = db.Column(db.String(255), nullable=False)

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='imagenes_usuarios')