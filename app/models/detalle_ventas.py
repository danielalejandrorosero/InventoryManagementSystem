from app import db

class DetalleVentas(db.Model):  # Corregido: faltaba db.Model
    __tablename__ = 'detalle_ventas'

    id_detalle_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta', ondelete='CASCADE'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto', ondelete='CASCADE'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False, default=0.0)
    precio_unitario = db.Column(db.Float, nullable=False, default=0.0)
    subtotal = db.Column(db.Float, nullable=False, default=0.0)

    # Relaciones
    venta = db.relationship('Ventas', back_populates='detalles')
    producto = db.relationship('Producto', back_populates='detalle_ventas')