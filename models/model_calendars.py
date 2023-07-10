from datetime import datetime
import sqlite3
from flask import jsonify

from gestor_jwt import token_required

DATABASE = "database/F5Vacances.sqlite"

class Calendars:
    def __init__(self, id, dateCal, approved):
        self.id = id
        self.dateCal = dateCal
        self.approved = approved

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS
            "calendars" (
                "id" INTEGER NOT NULL UNIQUE,
                "dateCal" TEXT NOT NULL,
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
    def post_calendar(cls, calendar):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('''INSERT INTO calendars (dateCal, approved)
                         VALUES (?, ?)''',
                      (calendar["dateCal"], calendar["approved"]))
            conn.commit()
            return jsonify({'message': 'calendar created successfully'}), 200
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def get_calendar_by_id(cls, calendar_id):
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("SELECT * FROM calendars WHERE id=?", (calendar_id,))
            result = c.fetchone()
            if result:
                calendar = {
                    "id": result[0],
                    "dateCal": result[1],
                    "approved": result[2]
                }
                return calendar
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def get_all_calendars(cls):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM calendars")
            results = c.fetchall()
            calendars = []
            for result in results:
                calendar = {
                    "id": result[0],
                    "dateCal": result[1],
                    "approved": result[2]
                }
                calendars.append(calendar)
            return calendars

        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def put_calendar(cls, data, calendar_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute('''UPDATE calendars SET dateCal=?, approved=?
                         WHERE id=?''',
                      (data['dateCal'], data['approved'], calendar_id))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()

    @classmethod
    @token_required
    def delete_calendar(cls, calendar_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("DELETE FROM calendars WHERE id=?", (calendar_id,))
            conn.commit()
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()

    @classmethod
    @token_required
    def patch_calendar(cls, data, calendar_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            update_query = "UPDATE calendars SET "
            params = []
            for key, value in data.items():
                update_query += f"{key}=?, "
                params.append(value)
            update_query = update_query[:-2]  # Eliminar la coma y el espacio extra al final
            update_query += " WHERE id=?"
            params.append(calendar_id)
            c.execute(update_query, tuple(params))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()
