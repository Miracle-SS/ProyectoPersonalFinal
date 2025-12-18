from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite que tu HTML haga fetch

# --- Conexión a la base de datos ---
conn = sqlite3.connect("registros.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS torneos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipo TEXT,
    capitan TEXT,
    correo TEXT,
    juego TEXT,
    mensaje TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    servicio TEXT,
    mensaje TEXT
)
""")
conn.commit()

# --- Rutas para registrar datos ---
@app.route("/registro_torneo", methods=["POST"])
def registro_torneo():
    data = request.form
    cursor.execute("INSERT INTO torneos (equipo, capitan, correo, juego, mensaje) VALUES (?, ?, ?, ?, ?)",
                   (data['equipo'], data['capitan'], data['correo'], data['juego'], data.get('mensaje','')))
    conn.commit()
    return jsonify({"status":"ok"})

@app.route("/registro_servicio", methods=["POST"])
def registro_servicio():
    data = request.form
    cursor.execute("INSERT INTO servicios (nombre, servicio, mensaje) VALUES (?, ?, ?)",
                   (data['nombre'], data['servicio'], data.get('mensaje','')))
    conn.commit()
    return jsonify({"status":"ok"})

# --- Rutas para que admin vea los registros ---
@app.route("/admin/torneos")
def admin_torneos():
    cursor.execute("SELECT * FROM torneos")
    return jsonify(cursor.fetchall())

@app.route("/admin/servicios")
def admin_servicios():
    cursor.execute("SELECT * FROM servicios")
    return jsonify(cursor.fetchall())

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/registros-torneos")
def registros_torneos():
    torneos = obtener_torneos()  # Función que consulta la DB
    return jsonify(torneos)

@app.route("/registros-servicios")
def registros_servicios():
    servicios = obtener_servicios()  # Función que consulta la DB
    return jsonify(servicios)