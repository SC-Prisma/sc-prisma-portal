Python
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
    if rol == "Profesional / Educador / Terapeuta":
        return f"""
        👩‍⚕️ **Bienvenid@ a la Red Profesional SC-Prisma**
        Hola {nombre_adulto}, recuerda que como profesional gestionas tu Oficina PRO y emites códigos para las familias.
        """
    else:
        usuarios_previos = db.collection('estudiantes').where('email', '==', email_adulto).get()
        
        if len(usuarios_previos) > 0:
            return f"""
            ⏳ **Hola nuevamente, {nombre_adulto}.**
            Notamos que el correo `{email_adulto}` ya disfrutó de su período de prueba gratuito de 3 días para {nombre_estudiante}. 
            Para continuar disfrutando de las aplicaciones y mantener el Ecosistema Digital activo, te invitamos a elegir una de nuestras opciones en https://sc-prisma.com/ecosistema-digital.html#pricing
            """
        
        prefijo = nombre_estudiante.split()[0][:3].upper()
        codigo_vip = f"{prefijo}{random.randint(1000, 9999)}VIP"
        
        hoy = datetime.now()
        vencimiento = hoy + timedelta(days=3)
        
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
            'fecha_vencimiento': vencimiento.strftime("%d/%m/%Y"),
            'codigo_vip': codigo_vip,
            'profesionalId': 'consultora', 
            'estado_acceso': 'Activo'
        }
        
        db.collection('estudiantes').add(nuevo_ecosistema_libre)
        
        return f"""
        🌟 **¡Tu Ecosistema para {nombre_estudiante} está listo!** 🌟
        
        Hola {nombre_adulto}. Nos alegra acompañarte. Tu correo `{email_adulto}` ha quedado registrado con éxito.
        
        🔑 **Tu Código VIP Personal es:** `{codigo_vip}`
        ⏳ **Vigencia:** 3 días (Hasta el {vencimiento.strftime('%d/%m/%Y')}).
        
        ---
        
        📌 **¿Cómo ingresar al Ecosistema Digital completo?**
        1. Dirígete a la página principal de nuestros ecosistemas.
        2. Busca la sección o botón de **"Inicia sesión VIP"**.
        3. Introduce tu código `{codigo_vip}` para ingresar directamente al espacio de {nombre_estudiante}.
        
        🚀 **¿Y las Aplicaciones Educativas?**
        ¡Este mismo código te sirve por 3 días para probar nuestras apps de forma gratuita! Explora y elige tus herramientas favoritas en nuestra **Biblioteca de Software**: 
        👉 https://sc-prisma.com/biblioteca-software/biblioteca-software.html
        
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
    outputs=gr.Textbox(label="Respuesta y Tus Accesos SC-Prisma", lines=16),
    title="✨ Formulario para Solicitud de Prueba Gratuita | SC-Prisma",
    description="Completa los datos para activar tus 3 días de acceso al Ecosistema Digital y a las Apps Educativas.",
    theme="soft"
)

# Lanzamiento para la nube en Render
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
