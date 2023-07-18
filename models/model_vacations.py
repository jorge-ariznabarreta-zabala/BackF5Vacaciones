from datetime import datetime
import sqlite3
from flask import jsonify
import jwt
from gestor_jwt import token_required

DATABASE = "database/F5Vacances.sqlite"

class Vacations:
    def __init__(self, id, id_user, list_days, approved):
        self.id = id
        self.id_user = id_user
        self.list_days = list_days
        self.approved = approved

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS
            "vacations" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_user" INTEGER NOT NULL,
                "list_days" TEXT NOT NULL,
                "approved" TEXT DEFAULT 'TRUE',
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
    def post_vacation(cls, vacation):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('''INSERT INTO vacations (id_user, list_days, approved)
                         VALUES (?, ?, ?)''',
                      (vacation["id_user"], vacation["list_days"], vacation["approved"]))
            conn.commit()
            return jsonify({'message': 'vacation created successfully'}), 200
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def get_vacation_by_id(cls, vacation_id):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM vacations WHERE id=?", (vacation_id,))
            result = c.fetchone()
            if result:
                vacation = {
                    "id": result[0],
                    "id_user": result[1],
                    "list_days": result[2],
                    "approved": result[3]
                }
                return vacation
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def get_all_vacations(cls):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM vacations")
            results = c.fetchall()
            vacations = []
            for result in results:
                vacation = {
                    "id": result[0],
                    "id_user": result[1],
                    "list_days": result[2],
                    "approved": result[3]
                }
                vacations.append(vacation)
            return vacations

        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def put_vacation(cls, data, vacation_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute('''UPDATE vacations SET id_user=?, list_days=?, approved=?
                         WHERE id=?''',
                      (data['id_user'], data['list_days'], data['approved'], vacation_id))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()

    @classmethod
    #@token_required
    def delete_vacation(cls, vacation_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("DELETE FROM vacations WHERE id=?", (vacation_id,))
            conn.commit()
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    #@token_required
    def patch_vacation(cls, data, vacation_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            update_query = "UPDATE vacations SET "
            params = []
            for key, value in data.items():
                update_query += f"{key}=?, "
                params.append(value)
            update_query = update_query[:-2]  # Eliminar la coma y el espacio extra al final
            update_query += " WHERE id=?"
            params.append(vacation_id)
            c.execute(update_query, tuple(params))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()
