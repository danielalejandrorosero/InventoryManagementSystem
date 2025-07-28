from app import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_producto = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False, unique=True)
    sku = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    precio_compra = db.Column(db.Float, nullable=False, default=0.0)
    precio_venta = db.Column(db.Float, nullable=False, default=0.0)
    id_unidad_medida = db.Column(db.Integer, db.ForeignKey('unidades_medida.id_unidad'), nullable=False)
    stock_minimo = db.Column(db.Float, nullable=False, default=0.0)
    stock_maximo = db.Column(db.Float, nullable=False, default=0.0)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria', ondelete='SET NULL'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)
    estado = db.Column(db.Enum('activo', 'eliminado'), nullable=False, default='activo')

    # Relaciones
    unidad_medida = db.relationship('UnidadMedida', back_populates='productos')
    categoria = db.relationship('Categoria', back_populates='productos')
    proveedor = db.relationship('Proveedor', back_populates='productos')
    stock_almacen = db.relationship('StockAlmacen', back_populates='producto', cascade='all, delete-orphan')
    alertas_stock = db.relationship('AlertasStock', back_populates='producto')
    detalle_compras = db.relationship('DetalleCompras', back_populates='producto', cascade='all, delete-orphan')
    detalle_ventas = db.relationship('DetalleVentas', back_populates='producto', cascade='all, delete-orphan')
    imagenes = db.relationship('ImagenesProductos', back_populates='producto', cascade='all, delete-orphan')
    movimientos_stock = db.relationship('MovimientosStock', back_populates='producto')