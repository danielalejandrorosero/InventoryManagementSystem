from app import db


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_categoria = db.Column(db.String(50), nullable=False)
    descripcion_categoria = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Enum('activo', 'eliminado'), nullable=False, default='activo')

    # Relaciones
    productos = db.relationship('Producto', back_populates='categoria', passive_deletes=True)


    # La categoría no existe
