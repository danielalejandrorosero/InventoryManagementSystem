from datetime import datetime, timedelta
from app import db
import secrets
from werkzeug.security import generate_password_hash
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    nombreUsuario = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)
    nivel_usuario = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    token_recuperacion = db.Column(db.String(255), nullable=True)
    expira_token = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    grupo = db.relationship('Grupo', back_populates='usuarios')
    imagenes_usuarios = db.relationship('ImagenesUsuarios', back_populates='usuario', cascade='all, delete-orphan')
    movimientos_stock = db.relationship('MovimientosStock', back_populates='usuario', cascade='all, delete-orphan')
    #chat_logs = db.relationship('ChatLogs', back_populates='usuario', passive_deletes=True)




    def generar_token_recuperacion(self):
        self.token_recuperacion = secrets.token_urlsafe(32)
        self.expira_token = datetime.utcnow() + timedelta(hours=1)
        return self.token_recuperacion
    

    def restablecer_password(self,password_nuevo):

        self.password = generate_password_hash(password_nuevo)
        self.token_recuperacion = None # Eliminar token de recuperación por que ya restableció la contraseña
        self.expira_token = None # lo mismo con la expiración y no hacemos return por que no queremos que el usuario vuelva a poder acceder a su cuenta con el token de recuperación
