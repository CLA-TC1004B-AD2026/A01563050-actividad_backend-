# pip install pymssql flask flask-cors requests
from flask import Flask, jsonify, request
import pymssql
import os

app = Flask(__name__)

# --- Configuración de la Conexión a MSSQL ---
SERVER = 'localhost'
DATABASE = 'master'
USERNAME = 'sa'
PASSWORD = 'YourPassword123!'

def get_db_connection():
    try:
        conn = pymssql.connect(
            server=SERVER,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE,
            charset='utf8'
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la DB: {e}")
        return None

# --- Rutas de la API (Servicios CRUD) ---

@app.route('/personajes', methods=['POST'])
def crear_personaje():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    
    if not nombre or not correo:
        return jsonify({"mensaje": "Faltan datos (nombre o correo)"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        # La tabla ya está creada con IDENTITY(1,1) para id. No se necesita @@IDENTITY en pymssql
        # si solo se necesita la confirmación de la inserción.
        sql = "INSERT INTO PersonajesShrek (nombre, correo) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, correo))
        conn.commit()
        return jsonify({"mensaje": "Personaje creado con éxito"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": f"Error al crear: {e}"}), 500
    finally:
        conn.close()


@app.route('/personajes', methods=['GET'])
def obtener_personajes():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cursor = conn.cursor(as_dict=True) # Retorna resultados como diccionarios
    try:
        sql = "SELECT id, nombre, correo FROM PersonajesShrek"
        cursor.execute(sql)
        personajes = cursor.fetchall()
        return jsonify(personajes), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al leer: {e}"}), 500
    finally:
        conn.close()


@app.route('/personajes/<int:id>', methods=['GET'])
def obtener_personaje(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cursor = conn.cursor(as_dict=True)
    try:
        sql = "SELECT id, nombre, correo FROM PersonajesShrek WHERE id = %s"
        cursor.execute(sql, (id,))
        personaje = cursor.fetchone()
        
        if personaje:
            return jsonify(personaje), 200
        return jsonify({"mensaje": "Personaje no encontrado"}), 404
    except Exception as e:
        return jsonify({"mensaje": f"Error al leer: {e}"}), 500
    finally:
        conn.close()


@app.route('/personajes/<int:id>', methods=['PUT'])
def actualizar_personaje(id):
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')

    if not nombre and not correo:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        # Prepara la consulta para actualizar solo los campos proporcionados
        updates = []
        params = []
        if nombre:
            updates.append("nombre = %s")
            params.append(nombre)
        if correo:
            updates.append("correo = %s")
            params.append(correo)

        if not updates:
            return jsonify({"mensaje": "No hay campos válidos para actualizar"}), 400
            
        sql = f"UPDATE PersonajesShrek SET {', '.join(updates)} WHERE id = %s"
        params.append(id)
        
        cursor.execute(sql, tuple(params))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"mensaje": "Personaje no encontrado o sin cambios"}), 404
            
        return jsonify({"mensaje": "Personaje actualizado con éxito"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": f"Error al actualizar: {e}"}), 500
    finally:
        conn.close()


@app.route('/personajes/<int:id>', methods=['DELETE'])
def eliminar_personaje(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"mensaje": "Error de conexión a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        sql = "DELETE FROM PersonajesShrek WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"mensaje": "Personaje no encontrado"}), 404
            
        return jsonify({"mensaje": "Personaje eliminado con éxito"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensaje": f"Error al eliminar: {e}"}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
