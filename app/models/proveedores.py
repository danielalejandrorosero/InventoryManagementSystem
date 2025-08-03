from app import db


class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_proveedor = db.Column(db.String(255), nullable=False)
    contacto = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)  # Cambiado a obligatorio
    estado = db.Column(db.Enum('activo', 'eliminado'), nullable=False, default='activo')

    # Relaciones
    productos = db.relationship('Producto', back_populates='proveedor', passive_deletes=True)
    compras = db.relationship('Compra', back_populates='proveedor', cascade='all, delete-orphan')
    movimientos_stock = db.relationship('MovimientosStock', back_populates='proveedor')
