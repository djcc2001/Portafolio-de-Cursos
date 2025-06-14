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


def enviar_notificacion_evaluacion(destinatario, nombre_docente, nombre_archivo, estado):
    remitente = 'portafolio.cursos.info@gmail.com'
    contraseña = 'zfsd sgax mwdt gzhb'

    if estado == "Aprobado":
        cuerpo = f"""Hola {nombre_docente},

Tu documento titulado '{nombre_archivo}' ha sido evaluado y ha sido **APROBADO**.

Puedes ingresar a la plataforma para revisar el estado de tu portafolio.

Saludos,
Equipo de Evaluación
"""
    else:
        cuerpo = f"""Hola {nombre_docente},

Tu documento titulado '{nombre_archivo}' ha sido evaluado y ha sido **DESAPROBADO**.

Por favor revisa las observaciones dejadas en la plataforma para poder realizar las correcciones necesarias.

Saludos,
Equipo de Evaluación
"""

    mensaje = MIMEText(cuerpo)
    mensaje['Subject'] = "Resultado de la Evaluación de tu Documento"
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)
    servidor.sendmail(remitente, destinatario, mensaje.as_string())
    servidor.quit()
