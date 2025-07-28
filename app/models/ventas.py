from app import db

class Ventas(db.Model):  # Corregido nombre de clase
    __tablename__ = 'ventas'

    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente', ondelete='SET NULL'), nullable=True)
    fecha_venta = db.Column(db.DateTime, nullable=False)
    total_venta = db.Column(db.Float, nullable=False, default=0.0)

    # Relaciones
    cliente = db.relationship('Cliente', back_populates='ventas')
    detalles = db.relationship('DetalleVentas', back_populates='venta', cascade='all, delete-orphan')
