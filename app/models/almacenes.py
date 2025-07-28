from app import db


class Almacen(db.Model):  # Corregido nombre de clase
    __tablename__ = 'almacenes'

    id_almacen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_almacen = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo'), nullable=False, default='activo')

    # Relaciones
    stock_almacen = db.relationship('StockAlmacen', back_populates='almacen', cascade='all, delete-orphan')
    alertas_stock = db.relationship('AlertasStock', back_populates='almacen', cascade='all, delete-orphan')

    movimientos_origen = db.relationship('MovimientosStock', foreign_keys='MovimientosStock.id_almacen_origen',
                                         back_populates='almacen_origen')
    movimientos_destino = db.relationship('MovimientosStock', foreign_keys='MovimientosStock.id_almacen_destino',
                                          back_populates='almacen_destino')
