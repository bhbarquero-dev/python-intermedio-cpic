from flask import Flask, request, jsonify
import pyodbc

# python.exe -m pip install --upgrade pip 
# pip install pyodbc

app = Flask(__name__)

# Configuración de conexión a la base de datos
server = '192.168.50.11'  # Puede ser una dirección IP o un nombre de servidor
database = 'PruebasCPIC'
username = 'pruebascpic'
password = 'Sql2016!CPIC0007$'

# Función para obtener la conexión
def get_db_connection():
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        return connection
    except pyodbc.Error as e:
        print("Error al conectar:", e)
        return None

# Endpoint para actualizar un activo
@app.route('/activos/<int:activo_id>', methods=['PUT'])
def actualizar_activo(activo_id):
    # Obtener datos del cuerpo de la solicitud
    datos = request.get_json()
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    estado = datos.get('estado')

    if not (nombre or descripcion or estado):
        return jsonify({"error": "Debe proporcionar al menos un campo para actualizar"}), 400

    # Conectar a la base de datos
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()

        # Construir la consulta dinámica
        campos = []
        if nombre:
            campos.append(f"nombre = '{nombre}'")
        if descripcion:
            campos.append(f"descripcion = '{descripcion}'")
        if estado:
            campos.append(f"estado = '{estado}'")

        consulta = f"UPDATE activos_ti SET {', '.join(campos)} WHERE id = ?"
        cursor.execute(consulta, (activo_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "No se encontró un activo con el ID proporcionado"}), 404

        return jsonify({"message": "Activo actualizado exitosamente"}), 200

    except pyodbc.Error as e:
        print("Error al ejecutar la consulta:", e)
        return jsonify({"error": "Error al actualizar el activo"}), 500

    finally:
        connection.close()

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
