from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

#======================================================================
# PANEL DE CONTROL - ¡EDITA ESTA SECCIÓN CON TUS CURSOS!
#======================================================================
# Aquí añades, quitas o modificas los cursos. 
# Usa una palabra clave simple (ej. "pixie") para que el bot la reconozca.
cursos_db = {
    "pixie": {
        "nombre_completo": "Corte Pixie Avanzado",
        "precio": "47€",
        "url": "https://www.masterhair.academy/curso/pixie" # O la URL específica del curso
    },
    "balayage": {
        "nombre_completo": "Experto en Balayage",
        "precio": "67€",
        "url": "https://www.masterhair.academy/curso/balayage"
    },
    # Añade aquí más cursos siguiendo el mismo formato
    # "palabra_clave": {
    #    "nombre_completo": "Nombre Del Curso",
    #    "precio": "XX€",
    #    "url": "https://link-al-curso.com"
    # }
}

# Respuestas para palabras clave generales
respuestas_generales = {
    "certificado": "¡Sí, por supuesto! Al completar el curso generas tu certificado personalizado para descargar. Así de fácil. ✨",
    "cupones": "¡Claro! Lanzamos cupones y ofertas exclusivas en nuestro Instagram @masterhair.academy y en la newsletter. ¡Síguenos para no perderte nada! 😉",
    "gamificacion": "Es nuestro sistema para que aprender sea más divertido. Ganas puntos y medallas al avanzar en los cursos 🏅. ¡Puedes ver tu progreso en tu perfil de alumno!",
    "gracias": "¡A ti! Para eso estamos. 😊"
}
#======================================================================
# FIN DEL PANEL DE CONTROL
#======================================================================


@app.route("/bot", methods=['POST'])
def bot():
    mensaje_usuario = request.form.get('Body').lower().strip()
    respuesta_final = ""

    # 1. El bot busca si el mensaje contiene la palabra clave de algún curso
    curso_encontrado = None
    for clave_curso in cursos_db.keys():
        if clave_curso in mensaje_usuario:
            curso_encontrado = cursos_db[clave_curso]
            break
    
    if curso_encontrado:
        # Si encuentra un curso, construye la respuesta personalizada
        respuesta_final = f"¡Claro! El curso '{curso_encontrado['nombre_completo']}' cuesta {curso_encontrado['precio']}. Puedes verlo en detalle aquí: {curso_encontrado['url']}"
    else:
        # 2. Si no, busca si el mensaje coincide con una palabra clave general
        respuesta_final = respuestas_generales.get(mensaje_usuario, "Lo siento, no te he entendido. Puedes preguntarme por el 'precio de pixie', 'certificado' o 'cupones' para que pueda ayudarte.")

    # Crea la respuesta para Twilio
    resp = MessagingResponse()
    resp.message(respuesta_final)
    return str(resp)

if __name__ == "__main__":
    # Esto permite que el bot se ejecute en tu ordenador para pruebas
    app.run(debug=True)