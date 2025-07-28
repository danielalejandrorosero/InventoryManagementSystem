from app import db

class StockAlmacen(db.Model):
    __tablename__ = 'stock_almacen'

    id_stock = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_almacen = db.Column(db.Integer, db.ForeignKey('almacenes.id_almacen', ondelete='CASCADE'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto', ondelete='CASCADE'), nullable=False)
    cantidad_disponible = db.Column(db.Float, nullable=False, default=0.0)

    # Relaciones
    producto = db.relationship('Producto', back_populates='stock_almacen')
    almacen = db.relationship('Almacen', back_populates='stock_almacen')