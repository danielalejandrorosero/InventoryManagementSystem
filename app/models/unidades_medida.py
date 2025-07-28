from app import db


class UnidadMedida(db.Model):
    __tablename__ = 'unidades_medida'

    id_unidad = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Corregido nombre
    nombre = db.Column(db.String(50), nullable=False)

    # Relaciones
    productos = db.relationship('Producto', back_populates='unidad_medida')