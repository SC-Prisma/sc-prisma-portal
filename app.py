import gradio as gr
from datetime import datetime, timedelta
import random
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Inicializar Firebase usando el secreto seguro de Render
if not firebase_admin._apps:
    firebase_secret_json = os.getenv("FIREBASE_KEY")
    cred_dict = json.loads(firebase_secret_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def portal_sc_prisma_con_marketing(rol, nombre_adulto, email_adulto, nombre_estudiante, edad_estudiante, motivo_apoyo, app_preferida):
    usuarios_previos = db.collection('estudiantes').where('email', '==', email_adulto).get()
    
    if len(usuarios_previos) > 0:
        doc = usuarios_previos[0].to_dict()
        codigo_existente = doc.get('codigo_vip', 'N/A')
        vencimiento_existente = doc.get('fecha_vencimiento', 'N/A')
        
        return f"""
⏳ **Hola nuevamente, {nombre_adulto}.**

Notamos que el correo `{email_adulto}` ya cuenta con un registro previo en nuestro sistema. 
Para que no te quedes sin acceso, aquí tienes nuevamente tus datos activos:

🔑 **Tu Código VIP es:** `{codigo_existente}`
⏳ **Vigencia:** Hasta el {vencimiento_existente}

⚠️ **¡Importante!** Copia y guarda tu clave en un lugar seguro. Si la pierdes, no podrás disfrutar del acceso.

📌 **Enlaces Directos:**
• Ingresa al Ecosistema Digital en la plataforma principal con tu código.
• Explora la Biblioteca de Software: 👉 [Biblioteca de Software SC-Prisma](https://sc-prisma.com/biblioteca-software/biblioteca-software.html)
• Conoce la Red Profesional: 👉 [Solicitud Profesional SC-Prisma](https://sc-prisma.com/solicitud-profesional.html)

⚖️ *Al ingresar a las aplicaciones, aceptas los términos y condiciones de uso del Ecosistema.*
        """
    
    if rol == "Profesional / Educador / Terapeuta":
        prefijo = nombre_adulto.split()[0][:3].upper()
        codigo_vip = f"PRO{prefijo}{random.randint(1000, 9999)}"
    else:
        prefijo = nombre_estudiante.split()[0][:3].upper()
        codigo_vip = f"{prefijo}{random.randint(1000, 9999)}VIP"
        
    hoy = datetime.now()
    vencimiento = hoy + timedelta(days=3)
    fecha_venc_str = vencimiento.strftime('%d/%m/%Y')
    
    nuevo_registro = {
        'apoderado': nombre_adulto,
        'email': email_adulto,
        'nombre': nombre_estudiante if rol != "Profesional / Educador / Terapeuta" else f"Evaluación Profesional ({nombre_estudiante})",
        'edad': f"{edad_estudiante} años",
        'diagnostico': motivo_apoyo,
        'grupo': 'Acceso Directo Profesional' if rol == "Profesional / Educador / Terapeuta" else 'Acceso Directo Familias',
        'plan': 'Prueba',
        'app_contratada': app_preferida,
        'fecha_creacion': hoy.strftime("%d/%m/%Y"),
        'fecha_vencimiento': fecha_venc_str,
        'codigo_vip': codigo_vip,
        'profesionalId': 'consultora', 
        'estado_acceso': 'Activo'
    }
    
    db.collection('estudiantes').add(nuevo_registro)
    
    return f"""
🌟 **¡Tu Acceso para {nombre_estudiante if rol != "Profesional / Educador / Terapeuta" else nombre_adulto} está listo!** 🌟

Hola **{nombre_adulto}**. Tu registro se ha completado con éxito de forma inmediata.

🔑 **Tu Código VIP Personal es:** `{codigo_vip}`
⏳ **Vigencia:** 3 días (Hasta el {fecha_venc_str}).

⚠️ **¡Copia tu clave ahora mismo!** Si la pierdes, no podrás disfrutar del acceso a las herramientas.

---

📌 **¿Cómo ingresar al Ecosistema Digital completo?**
1. Dirígete a la página principal de nuestros ecosistemas e introduce tu código `{codigo_vip}` en la sección de inicio de sesión VIP.

🚀 **¿Y las Aplicaciones Educativas?**
Prueba tus apps de forma gratuita durante 3 días en nuestra **Biblioteca de Software**: 
👉 [Biblioteca de Software SC-Prisma](https://sc-prisma.com/biblioteca-software/biblioteca-software.html)

💼 **¿Eres Profesional y deseas tu Oficina PRO?**
Visita nuestra página de suscripción: 
👉 [Solicitud Profesional SC-Prisma](https://sc-prisma.com/solicitud-profesional.html)

⚖️ *Al hacer clic en activar y hacer uso de las aplicaciones, aceptas los términos y condiciones de uso del Ecosistema.*
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
    theme="soft",
    submit_btn="🚀 Activar Mi Prueba y Obtener Acceso"
)

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))
