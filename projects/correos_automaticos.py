from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from projects.utils import generar_qr_bytes





def enviar_correo_bienvenida(nombre, apellido, s_apellido, correo):
    
    # Capitalizar nombre y apellidos (la primera letra es mayúscula)
    nombre = nombre.capitalize()
    apellido = apellido.capitalize()
    s_apellido = s_apellido.capitalize()
    correo = correo.lower()    
    
    asunto = "Registro exitoso Bahía Bonita"
    mensaje_html = f"""
    <p>Estimado/a {nombre} {apellido} {s_apellido},</p>

    <p>Bienvenid@ a Bahía Bonita</p>
    
    <p>Nos alegra contar con tu confianza y estamos seguros de que disfrutarás de una experiencia cómoda y placentera junto a nosotros.</p>
    <p>Desde ya, puedes acceder a nuestro sitio para consultar disponibilidad, realizar reservas o resolver cualquier duda que tengas.</p>
    <a href="https://www.bahiabonita.cl" target="_blank">Visita nuestro sitio web</a>
    <p>¡Gracias por registrarse en <strong>Bahía Bonita</strong>!</p>

    Muchas gracias por preferirnos.<br>
    Bahía Bonita, Concón, Chile.<br>
    Si tiene alguna consulta, no dude en contactarnos<br>
    <strong> Tel: +56 9 3095 6242</strong>      
    """

    mensaje = EmailMultiAlternatives(
        asunto,
        "",  # mensaje de texto plano (vacío si solo HTML)
        settings.EMAIL_HOST_USER,
        [correo]  # destinatario
    )
    mensaje.attach_alternative(mensaje_html, "text/html")
    mensaje.send()

###############################################
    
def enviar_correo_reserva(nombre, apellido, s_apellido, correo, reserva):
    nombre = nombre.capitalize()
    apellido = apellido.capitalize()
    s_apellido = s_apellido.capitalize()
    correo = correo.lower()
    
    qr_data = f"Reserva ID: {reserva.id_reserva}, Cliente: {nombre} {apellido} {s_apellido}, Ingreso: {reserva.fecha_ingreso}, Salida: {reserva.fecha_salida}, Creado el: {reserva.fecha_creacion}"
    qr_buffer = generar_qr_bytes(qr_data)
    
    # Datos para el correo
    asunto = "Confirmación de Reserva – Bahía Bonita"
    mensaje_html = f"""
    <p>Estimado/a {nombre} {apellido} {s_apellido},</p>

    <p>Su reserva ha sido confirmada exitosamente.</p>

    <ul>
    <li><b>Departamento:</b> {reserva.departamento.num_depto}</li>
    <li><b>Creación de la reserva:</b> {reserva.fecha_reserva}</li>
    <li><b>Ingreso:</b> {reserva.fecha_ingreso}</li>
    <li><b>Salida:</b> {reserva.fecha_salida}</li>
    <li><b>Personas:</b> {reserva.cant_personas}</li>
    <li><b>Total:</b> ${reserva.valor_total:.0f}</li>
    </ul>

    <p><b> Muestra este código QR al llegar al check-in:</b></p>
    <img src="cid:qr_code" alt="Código QR de reserva" style="width:200px;height:200px;" />
    <br>

    Muchas gracias por preferirnos.<br>
    Bahía Bonita, Concón, Chile.<br>
    Si tiene alguna consulta, no dude en contactarnos<br>
    Tel: +56 9 3095 6242.      
    """
    

    # Enviar el correo
    email = EmailMultiAlternatives(
        subject=asunto,
        body=mensaje_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[correo],
    )

    email.attach_alternative(mensaje_html, "text/html")            

    # Adjuntar imagen como recurso embebido (inline)
    qr_image = MIMEImage(qr_buffer.getvalue(), _subtype="png")
    qr_image.add_header("Content-ID", "<qr_code>")  # <qr_code> se referencia en el HTML
    qr_image.add_header("Content-Disposition", "inline", filename="qr.png")
    email.attach(qr_image)

    # Enviar
    email.send()

################################################
# Función para enviar correo de bienvenida a colaboradores
def correo_bienvenida_colab (nombre, apellido, s_apellido, email, password):
    nombre = nombre.capitalize()
    apellido = apellido.capitalize()
    s_apellido = s_apellido.capitalize()
    email = email.lower()

    asunto = "Bienvenido a Bahía Bonita"
    mensaje_html = f"""
    <p>Estimado/a {nombre} {apellido} {s_apellido},</p>

    <p>¡Bienvenido/a a Bahía Bonita!</p>
    
    <p>Estamos encantados de tenerte con nosotros. Tu cuenta ha sido creada exitosamente.</p>
    
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Contraseña:</strong> {password}</p>

    <p>Te invitamos a iniciar sesión y explorar todas las funcionalidades que ofrecemos.</p>
    
    Muchas gracias por unirte a nosotros.<br>
    Bahía Bonita, Concón, Chile.<br>
    Si tienes alguna consulta, no dudes en contactarnos<br>
    Tel: +56 9 3095 6242
    """

    mensaje = EmailMultiAlternatives(
        asunto,
        "",  # mensaje de texto plano (vacío si solo HTML)
        settings.EMAIL_HOST_USER,
        [email]  # destinatario
    )
    mensaje.attach_alternative(mensaje_html, "text/html")
    mensaje.send()