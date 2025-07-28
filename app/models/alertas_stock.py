from app import db

class AlertasStock(db.Model):
    __tablename__ = 'alertas_stock'

    id_alerta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_almacen = db.Column(db.Integer, db.ForeignKey('almacenes.id_almacen', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    fecha_alerta = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Enum('pendiente', 'enviada'), nullable=False, default='pendiente')

    # Relaciones
    producto = db.relationship('Producto', back_populates='alertas_stock')
    almacen = db.relationship('Almacen', back_populates='alertas_stock')        