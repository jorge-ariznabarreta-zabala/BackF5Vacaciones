from datetime import datetime
import sqlite3
from flask import jsonify
import jwt
from gestor_jwt import token_required

DATABASE = "database/F5Vacances.sqlite"

class Workers:
    def __init__(self, id, name, position, seniority, department, email, passw):
        self.id = id
        self.name = name
        self.position = position
        self.seniority = seniority
        self.department = department
        self.email = email
        self.passw = passw

    @classmethod
    def login(cls, email, passw):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM workers WHERE email=?", (email,))
            result = c.fetchone();
            print(result)
            if result and result[6] == passw:  # Verificar si se encontró el usuario y la contraseña coincide
                secret = str(datetime.now().timestamp())
                worker = {
                    "id": result[0],
                    "name": result[1],
                    "position": result[2],
                    "seniority": result[3],
                    "department": result[4],
                    "email": result[5],
                    "passw": result[6]
                }
                token = Workers.generate_token(worker, secret)
                print ("LOGIN", worker, token, secret)
                return worker, token, secret
            else:
                return ({"error": "Credenciales inválidas"}), 401

        except sqlite3.Error as e:
            return ({"SQLError": str(e)}, 500)
        finally:
            conn.close()

    @classmethod
    def generate_token(cls, user, secret):
        token = jwt.encode({
            "id": user["id"],
            "name": user["name"],
            "position": user["position"],
            "seniority": user["seniority"],
            "department": user["department"],
            "email": user["email"],
            "passw": user["passw"]
        }, secret)
        return token

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS
            "workers" (
                "id" INTEGER NOT NULL UNIQUE,
                "name" TEXT NOT NULL,
                "position" TEXT,
                "seniority" TEXT,
                "department" TEXT,
                "email" TEXT NOT NULL,
                "passw" TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    #@token_required
    def post_worker(cls, worker):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('''INSERT INTO workers (name, position, seniority, department, email, passw)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (worker["name"], worker["position"], worker["seniority"], worker["department"],
                       worker["email"], worker["passw"]))
            conn.commit()
            return jsonify({'message': 'worker created successfully'}), 200
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def get_worker_by_id(cls, worker_id):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM workers WHERE id=?", (worker_id,))
            result = c.fetchone()
            if result:
                worker = {
                    "id": result[0],
                    "name": result[1],
                    "position": result[2],
                    "seniority": result[3],
                    "department": result[4],
                    "email": result[5],
                    "passw": result[6]
                }
                return worker
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def get_all_workers(cls):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM workers")
            results = c.fetchall()
            workers = []
            for result in results:
                worker = {
                    "id": result[0],
                    "name": result[1],
                    "position": result[2],
                    "seniority": result[3],
                    "department": result[4],
                    "email": result[5],
                    "passw": result[6]
                }
                workers.append(worker)
            return workers

        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def put_worker(cls, data, worker_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute('''UPDATE workers SET name=?, position=?, seniority=?, department=?, email=?, passw=?
                         WHERE id=?''',
                      (data['name'], data['position'], data['seniority'], data['department'],
                       data['email'], data['passw'], worker_id))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()

    @classmethod
    #@token_required
    def delete_worker(cls, worker_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("DELETE FROM workers WHERE id=?", (worker_id,))
            conn.commit()
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def patch_worker(cls, data, worker_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            update_query = "UPDATE workers SET "
            params = []
            for key, value in data.items():
                update_query += f"{key}=?, "
                params.append(value)
            update_query = update_query[:-2]  # Eliminar la coma y el espacio extra al final
            update_query += " WHERE id=?"
            params.append(worker_id)
            c.execute(update_query, tuple(params))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()
