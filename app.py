from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- BASE DE DATOS ----------------
def crear_bd():
    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        carnet TEXT NOT NULL,
        carrera TEXT NOT NULL,
        semestre TEXT NOT NULL,
        telefono TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()

# ---------------- LISTAR ----------------
@app.route("/")
def index():
    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()

    conexion.close()

    return render_template("index.html", estudiantes=estudiantes)

# ---------------- AGREGAR ----------------
@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    carnet = request.form["carnet"]
    carrera = request.form["carrera"]
    semestre = request.form["semestre"]
    telefono = request.form["telefono"]

    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO estudiantes(nombre, apellido, carnet, carrera, semestre, telefono)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, apellido, carnet, carrera, semestre, telefono))

    conexion.commit()
    conexion.close()

    return redirect("/")

# ---------------- BUSCAR ----------------
@app.route("/buscar")
def buscar():
    texto = request.args.get("texto")

    conexion = sqlite3.connect("estudiantes.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT * FROM estudiantes
    WHERE nombre LIKE ? OR apellido LIKE ? OR carnet LIKE ?
    """, (f"%{texto}%", f"%{texto}%", f"%{texto}%"))

    estudiantes = cursor.fetchall()

    conexion.close()

    return render_template("index.html", estudiantes=estudiantes)

if __name__ == "__main__":
    crear_bd()
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
