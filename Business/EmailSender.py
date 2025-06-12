import smtplib
from email.mime.text import MIMEText

def enviar_codigo_email(destinatario, codigo):
    remitente = 'correo-remitente@gmail.com'
    contraseña = 'clave-app'  # Usa clave de app si es Gmail
    mensaje = MIMEText(f"Tu código de verificación es: {codigo}")
    mensaje['Subject'] = "Código de recuperación"
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)
    servidor.sendmail(remitente, destinatario, mensaje.as_string())
    servidor.quit()
