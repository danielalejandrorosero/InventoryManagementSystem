from app import db


class Grupo(db.Model):
    __tablename__ = 'grupos'

    id_grupo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_grupo = db.Column(db.String(50), nullable=False)
    nivel_grupo = db.Column(db.Integer, nullable=False, default=1)
    estado = db.Column(db.Enum('activo', 'eliminado'), nullable=False, default='activo')

    # Relaciones
    usuarios = db.relationship('Usuario', back_populates='grupo', cascade='all, delete-orphan')




