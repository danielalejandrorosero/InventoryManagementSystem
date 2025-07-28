from flask_mail import Message
from flask import current_app

def enviar_email_recuperacion(destinatario, token):
    # Importar mail desde el contexto de la aplicación
    from app import mail
    
    try:
        url = f"http://localhost:5000/auth/restablecer?token={token}"
        
        # Crear mensaje con parámetros explícitos
        msg = Message(
            subject="Recuperación de contraseña",
            recipients=[destinatario],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        # Contenido HTML del correo
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Recuperación de Contraseña</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #f8f9fa;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">🔐 Recuperación de Contraseña</h1>
                </div>
                
                <div style="padding: 40px 30px; background-color: white;">
                    <h2 style="color: #333; margin-bottom: 20px;">¡Hola!</h2>
                    
                    <p style="color: #666; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                        Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.
                        Si fuiste tú quien la solicitó, haz clic en el botón de abajo para continuar.
                    </p>
                    
                    <div style="text-align: center; margin: 35px 0;">
                        <a href="{url}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 16px; display: inline-block;">
                            🔑 Restablecer Contraseña
                        </a>
                    </div>
                    
                    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 25px 0;">
                        <p style="color: #856404; margin: 0; font-size: 14px;">
                            ⏰ <strong>Importante:</strong> Este enlace expira en <strong>1 hora</strong> por tu seguridad.
                        </p>
                    </div>
                    
                    <p style="color: #666; font-size: 14px; line-height: 1.6; margin-top: 25px;">
                        Si no solicitaste este cambio, puedes ignorar este correo. Tu contraseña no será modificada.
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        Este es un correo automático, por favor no respondas a este mensaje.
                    </p>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
                    <p style="color: #999; font-size: 12px; margin: 0;">
                        © 2024 Tu Aplicación. Todos los derechos reservados.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # También incluir versión de texto plano
        msg.body = f"""
Recuperación de Contraseña

¡Hola!

Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.

Haz clic en el siguiente enlace para restablecer tu contraseña:
{url}

IMPORTANTE: Este enlace expira en 1 hora por tu seguridad.

Si no solicitaste este cambio, puedes ignorar este correo.

---
Este es un correo automático, por favor no respondas a este mensaje.
        """
        
        # Enviar el correo
        mail.send(msg)
        print(f"Correo enviado exitosamente a: {destinatario}")
        
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        print(f"Destinatario: {destinatario}")
        print(f"Token: {token}")
        import traceback
        traceback.print_exc()
        raise e