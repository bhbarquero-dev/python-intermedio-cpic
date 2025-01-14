from flask import Flask, request, jsonify
import mysql.connector
#pip install mysql-connector-python
















app = Flask(__name__)

# Configuración de la conexión a la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",       # Cambiar según tu configuración
        user="root",      # Usuario de MySQL
        password="",  # Contraseña del usuario
        database="test"   # Nombre de la base de datos
    )








# Rutas y lógica de la API
@app.route('/', methods=['GET'])
def index():
    return "Mi Rest API con MySQL"











# GET: Obtener una persona por ID
@app.route("/persona/<int:id>", methods=['GET'])
def obtener_persona(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, apellidos FROM personas WHERE id = %s", (id,))
    persona = cursor.fetchone()
    conexion.close()

    if persona:
        return jsonify(persona), 200
    else:
        return jsonify({"error": "Persona no encontrada"}), 404


# POST: Crear una nueva persona
@app.route("/persona", methods=['POST'])
def crear_persona():
    datos = request.get_json()

    # Validar los datos enviados
    if not datos or "nombre" not in datos or "apellidos" not in datos:
        return jsonify({"error": "Datos inválidos. Se requiere 'nombre' y 'apellidos'"}), 400

    nombre = datos["nombre"]
    apellidos = datos["apellidos"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO personas (nombre, apellidos) VALUES (%s, %s)", (nombre, apellidos))
    conexion.commit()
    persona_id = cursor.lastrowid
    conexion.close()

    return jsonify({
        "id": persona_id,
        "nombre": nombre,
        "apellidos": apellidos,
        "estado": "creado"
    }), 201


# PUT: Actualizar una persona por ID
@app.route("/persona/<int:id>", methods=['PUT'])
def actualizar_persona(id):
    datos = request.get_json()

    # Validar los datos enviados
    if not datos or "nombre" not in datos or "apellidos" not in datos:
        return jsonify({"error": "Datos inválidos. Se requiere 'nombre' y 'apellidos'"}), 400

    nombre = datos["nombre"]
    apellidos = datos["apellidos"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE personas SET nombre = %s, apellidos = %s WHERE id = %s",
        (nombre, apellidos, id)
    )
    conexion.commit()
    filas_actualizadas = cursor.rowcount
    conexion.close()

    if filas_actualizadas == 0:
        return jsonify({"error": "Persona no encontrada"}), 404

    return jsonify({
        "id": id,
        "nombre": nombre,
        "apellidos": apellidos,
        "estado": "actualizado"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
