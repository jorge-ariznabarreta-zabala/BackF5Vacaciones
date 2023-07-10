from datetime import datetime
import sqlite3
from flask import jsonify
import jwt
from gestor_jwt import token_required

DATABASE = "database/F5Vacances.sqlite"

class Vacations:
    def __init__(self, id, id_user, id_calendar, approved):
        self.id = id
        self.id_user = id_user
        self.id_calendar = id_calendar
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
                "id_calendar" INTEGER NOT NULL,
                "approved" INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
            );''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    @token_required
    def post_vacance(cls, vacance):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('''INSERT INTO vacations (id_user, id_calendar, approved)
                         VALUES (?, ?, ?)''',
                      (vacance["id_user"], vacance["id_calendar"], vacance["approved"]))
            conn.commit()
            return jsonify({'message': 'vacance created successfully'}), 200
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def get_vacance_by_id(cls, vacance_id):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM vacations WHERE id=?", (vacance_id,))
            result = c.fetchone()
            if result:
                vacance = {
                    "id": result[0],
                    "id_user": result[1],
                    "id_calendar": result[2],
                    "approved": result[3]
                }
                return vacance
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def get_all_vacations(cls):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM vacations")
            results = c.fetchall()
            vacations = []
            for result in results:
                vacance = {
                    "id": result[0],
                    "id_user": result[1],
                    "id_calendar": result[2],
                    "approved": result[3]
                }
                vacations.append(vacance)
            return vacations

        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def put_vacance(cls, data, vacance_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute('''UPDATE vacations SET id_user=?, id_calendar=?, approved=?
                         WHERE id=?''',
                      (data['id_user'], data['id_calendar'], data['approved'], vacance_id))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()

    @classmethod
    @token_required
    def delete_vacance(cls, vacance_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("DELETE FROM vacations WHERE id=?", (vacance_id,))
            conn.commit()
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def patch_vacance(cls, data, vacance_id):
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
            params.append(vacance_id)
            c.execute(update_query, tuple(params))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()
