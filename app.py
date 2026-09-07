import gradio as gr
from datetime import datetime, timedelta
import random
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Inicializar Firebase usando el secreto seguro de Render
if not firebase_admin._apps:
    firebase_secret_json = os.getenv("FIREBASE_KEY")
    cred_dict = json.loads(firebase_secret_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def enviar_correo_respaldo(destinatario, nombre_usuario, codigo, tipo_usuario, vencimiento):
    remitente = os.getenv("MAIL_USER")
    password = os.getenv("MAIL_PASSWORD")
    
    if not remitente or not password:
        return False  # Si no están configuradas las credenciales, omite el envío para evitar errores en la app
    
    try:
        asunto = "✨ Tus Accesos y Código VIP - SC-Prisma"
        
        cuerpo = f"""
Hola {nombre_usuario},

Nos alegra mucho acompañarte en el Ecosistema SC-Prisma. 

A continuación, tienes el respaldo de tus datos de acceso para tu período de prueba de 3 días:

🔑 Tu Código VIP: {codigo}
⏳ Vigencia: Hasta el {vencimiento}
👤 Perfil: {tipo_usuario}

---

📌 Enlaces de Acceso Importantes:
• Ingresa al Ecosistema Digital con tu código en la plataforma principal.
• Explora la Biblioteca de Software: https://sc-prisma.com/biblioteca-software/biblioteca-software.html
• Conoce la Red Profesional: https://sc-prisma.com/solicitud-profesional.html

---

⚖️ TÉRMINOS Y CONDICIONES DE USO:
Al ingresar y hacer uso de las distintas aplicaciones y herramientas del Ecosistema Digital de SC-Prisma, el usuario acepta expresamente los términos de uso, políticas de privacidad y los límites de las licencias temporales de prueba. El código es de uso personal e intransferible.

¡Que comience la aventura hacia un aprendizaje sin frustraciones!

Atentamente,
El Equipo de SC-Prisma
"""

        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain'))

        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def portal_sc_prisma_con_marketing(rol, nombre_adulto, email_adulto, nombre_estudiante, edad_estudiante, motivo_apoyo, app_preferida):
    if rol == "Profesional / Educador / Terapeuta":
        usuarios_previos = db.collection('estudiantes').where('email', '==', email_adulto).get()
        
        if len(usuarios_previos) > 0:
            return f"""
⏳ **Hola nuevamente, {nombre_adulto}.**

Notamos que el correo `{email_adulto}` ya disfrutó de su período de prueba gratuito profesional. 
Para adquirir tu Oficina PRO y emitir códigos ilimitados para tus familias, suscríbete visitando nuestra página oficial:
👉 [Solicitud Profesional SC-Prisma](https://sc-prisma.com/solicitud-profesional.html)
            """
        
        prefijo = nombre_adulto.split()[0][:3].upper()
        codigo_vip = f"PRO{prefijo}{random.randint(1000, 9999)}"
        
        hoy = datetime.now()
        vencimiento = hoy + timedelta(days=3)
        fecha_venc_str = vencimiento.strftime('%d/%m/%Y')
        
        nuevo_registro_profesional = {
            'apoderado': nombre_adulto,
            'email': email_adulto,
            'nombre': f"Evaluación Profesional ({nombre_estudiante})",
            'edad': f"{edad_estudiante} años",
            'diagnostico': motivo_apoyo,
            'grupo': 'Acceso Directo Profesional',
            'plan': 'Prueba Profesional',
            'app_contratada': app_preferida,
            'fecha_creacion': hoy.strftime("%d/%m/%Y"),
            'fecha_vencimiento': fecha_venc_str,
            'codigo_vip': codigo_vip,
            'profesionalId': 'red-profesional', 
            'estado_acceso': 'Activo'
        }
        
        db.collection('estudiantes').add(nuevo_registro_profesional)
        
        # Enviar correo de respaldo automático
        enviar_correo_respaldo(email_adulto, nombre_adulto, codigo_vip, "Profesional / Terapeuta", fecha_venc_str)
        
        return f"""
👩‍💼 **¡Bienvenid@ a la Red Profesional SC-Prisma, {nombre_adulto}!** 👩‍💼

Tu registro y tu período de prueba gratuito de **3 días** se han activado con éxito. 
Te hemos enviado un **correo de respaldo** a `{email_adulto}` con tu clave y los términos de uso.

🔑 **Tu Código VIP Profesional es:** `{codigo_vip}`
⏳ **Vigencia:** Hasta el {fecha_venc_str}.

---

📌 **¿Cómo evaluar el Ecosistema del Estudiante?**
1. Dirígete a la página principal de nuestros ecosistemas.
2. Introduce tu código `{codigo_vip}` en la opción de inicio de sesión VIP.

🚀 **¿Y la Biblioteca de Aplicaciones?**
Puedes explorar todas las herramientas interactivas utilizando este mismo código en nuestra **Biblioteca de Software**: 
👉 [Biblioteca de Software SC-Prisma](https://sc-prisma.com/biblioteca-software/biblioteca-software.html)

💼 **¿Deseas gestionar tu propia Oficina PRO?**
Para conectar este entorno con una oficina virtual y emitir códigos personalizados a tus familias, suscríbete a un plan visitando: 
👉 [Solicitud Profesional SC-Prisma](https://sc-prisma.com/solicitud-profesional.html)

⚖️ *Al ingresar a las aplicaciones, aceptas los términos y condiciones de uso del Ecosistema.*
        """
    else:
        usuarios_previos = db.collection('estudiantes').where('email', '==', email_adulto).get()
        
        if len(usuarios_previos) > 0:
            return f"""
⏳ **Hola nuevamente, {nombre_adulto}.**

Notamos que el correo `{email_adulto}` ya disfrutó de su período de prueba gratuito de 3 días para {nombre_estudiante}. 
Para continuar disfrutando de las aplicaciones y mantener el Ecosistema Digital activo, te invitamos a elegir una de nuestras opciones en:
👉 [Planes y Opciones Ecosistema Digital](https://sc-prisma.com/ecosistema-digital.html#pricing)
            """
        
        prefijo = nombre_estudiante.split()[0][:3].upper()
        codigo_vip = f"{prefijo}{random.randint(1000, 9999)}VIP"
        
        hoy = datetime.now()
        vencimiento = hoy + timedelta(days=3)
        fecha_venc_str = vencimiento.strftime('%d/%m/%Y')
        
        nuevo_ecosistema_libre = {
            'apoderado': nombre_adulto,
            'email': email_adulto,
            'nombre': nombre_estudiante,
            'edad': f"{edad_estudiante} años",
            'diagnostico': motivo_apoyo,
            'grupo': 'Acceso Directo Familias',
            'plan': 'Prueba',
            'app_contratada': app_preferida,
            'fecha_creacion': hoy.strftime("%d/%m/%Y"),
            'fecha_vencimiento': fecha_venc_str,
            'codigo_vip': codigo_vip,
            'profesionalId': 'consultora', 
            'estado_acceso': 'Activo'
        }
        
        db.collection('estudiantes').add(nuevo_ecosistema_libre)
        
        # Enviar correo de respaldo automático
        enviar_correo_respaldo(email_adulto, nombre_adulto, codigo_vip, f"Familiar ({nombre_estudiante})", fecha_venc_str)
        
        return f"""
🌟 **¡Tu Ecosistema para {nombre_estudiante} está listo!** 🌟

Hola **{nombre_adulto}**. Nos alegra acompañarte. Tu correo `{email_adulto}` ha quedado registrado con éxito.
Te hemos enviado un **correo de respaldo** con tu clave para que no la pierdas.

🔑 **Tu Código VIP Personal es:** `{codigo_vip}`
⏳ **Vigencia:** 3 días (Hasta el {fecha_venc_str}).

---

📌 **¿Cómo ingresar al Ecosistema Digital completo?**
1. Dirígete a la página principal de nuestros ecosistemas.
2. Busca la sección o botón de **"Inicia sesión VIP"**.
3. Introduce tu código `{codigo_vip}` para ingresar directamente al espacio de {nombre_estudiante}.

🚀 **¿Y las Aplicaciones Educativas?**
¡Este mismo código te sirve por 3 días para probar nuestras apps de forma gratuita! Explora y elige tus herramientas favoritas en nuestra **Biblioteca de Software**: 
👉 [Biblioteca de Software SC-Prisma](https://sc-prisma.com/biblioteca-software/biblioteca-software.html)

⚖️ *Al ingresar y hacer uso de las distintas aplicaciones, aceptas los términos y condiciones de uso del Ecosistema.*

¡Que comience la aventura hacia un aprendizaje sin frustraciones!
        """

demo = gr.Interface(
    fn=portal_sc_prisma_con_marketing,
    inputs=[
        gr.Radio(["Padre / Apoderado", "Profesional / Educador / Terapeuta"], label="Selecciona tu perfil:", value="Padre / Apoderado"),
        gr.Textbox(label="Tu Nombre Completo", placeholder="Ej. Clargina Monsalve"),
        gr.Textbox(label="Correo Electrónico", placeholder="correo@familia.com"),
        gr.Textbox(label="Nombre del Estudiante", placeholder="Ej. Mateo"),
        gr.Number(label="Edad del Estudiante", value=6, precision=0),
        gr.Textbox(label="Motivo Principal de Apoyo", placeholder="Ej. TEA, TDAH, communication..."),
        gr.Dropdown(
            choices=[
                "Tablero Aurora SAAC (Recomendado)", 
                "Ecosistema Completo de Seguimiento Conductual-Sensorial", 
                "Prisma-Track Bitácora", 
                "GrafiLees Aventura", 
                "AstroMath"
            ], 
            label="Herramienta a priorizar en tu prueba", 
            value="Tablero Aurora SAAC (Recomendado)"
        )
    ],
    outputs=gr.Markdown(label="Respuesta y Tus Accesos SC-Prisma"),
    title="✨ Formulario para Solicitud de Prueba Gratuita | SC-Prisma",
    description="Completa los datos para activar tus 3 días de acceso al Ecosistema Digital y a las Apps Educativas.",
    theme="soft"
)

# Lanzamiento para la nube en Render
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))
