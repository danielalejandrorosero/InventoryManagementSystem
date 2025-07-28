from app import db

class DetalleCompras(db.Model):
    __tablename__ = 'detalle_compras'

    id_detalle_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('compras.id_compra', ondelete='CASCADE'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto', ondelete='CASCADE'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Relaciones
    compra = db.relationship('Compra', back_populates='detalles')
    producto = db.relationship('Producto', back_populates='detalle_compras')