from app import db
class MovimientosStock(db.Model):  # Corregido: faltaba db.Model
    __tablename__ = 'movimientos_stock'  # Corregido: faltaba __

    id_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)  # Agregado campo faltante
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=True)
    id_almacen_origen = db.Column(db.Integer, db.ForeignKey('almacenes.id_almacen'), nullable=True)  # Corregido FK
    id_almacen_destino = db.Column(db.Integer, db.ForeignKey('almacenes.id_almacen'), nullable=True)  # Corregido FK
    cantidad = db.Column(db.Float, nullable=False, default=0.0)
    fecha_movimiento = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)

    # Relaciones
    producto = db.relationship('Producto', back_populates='movimientos_stock')
    proveedor = db.relationship('Proveedor', back_populates='movimientos_stock')
    almacen_origen = db.relationship('Almacen', foreign_keys=[id_almacen_origen], back_populates='movimientos_origen')
    almacen_destino = db.relationship('Almacen', foreign_keys=[id_almacen_destino], back_populates='movimientos_destino')
    usuario = db.relationship('Usuario', back_populates='movimientos_stock')