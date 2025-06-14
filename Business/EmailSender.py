import smtplib
from email.mime.text import MIMEText

def enviar_codigo_email(destinatario, codigo):
    remitente = 'portafolio.cursos.info@gmail.com'
    contraseña = 'zfsd sgax mwdt gzhb'  # Usa clave de app si es Gmail
    mensaje = MIMEText(f"Tu código de verificación es: {codigo}")
    mensaje['Subject'] = "Código de recuperación"
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)
    servidor.sendmail(remitente, destinatario, mensaje.as_string())
    servidor.quit()

def enviar_notificacion_asignacion(destinatario, nombre_evaluador, nombre_archivo):
    remitente = 'portafolio.cursos.info@gmail.com'
    contraseña = 'zfsd sgax mwdt gzhb'
    
    mensaje = MIMEText(
        f"Hola {nombre_evaluador},\n\nSe te ha asignado el trabajo: {nombre_archivo}.\n\nPor favor, revisa la plataforma para más detalles.\n\nGracias."
    )
    mensaje['Subject'] = "Nuevo trabajo asignado"
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)
    servidor.sendmail(remitente, destinatario, mensaje.as_string())
    servidor.quit()
