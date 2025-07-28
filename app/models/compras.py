from app import db

class Compra(db.Model):
    __tablename__ = 'compras'

    id_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor', ondelete='CASCADE'), nullable=False)
    fecha_compra = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    estado = db.Column(db.Enum('pendiente', 'completada', 'cancelada'), nullable=False, default='pendiente')

    # Relaciones
    proveedor = db.relationship('Proveedor', back_populates='compras')
    detalles = db.relationship('DetalleCompras', back_populates='compra', cascade='all, delete-orphan')
