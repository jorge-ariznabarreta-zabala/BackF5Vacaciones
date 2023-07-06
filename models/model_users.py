from datetime import datetime
import sqlite3
from flask import jsonify
import jwt
from gestor_jwt import token_required

DATABASE= "database/OV.sqlite"

class Users:
    def __init__(self, id, login_email, passw, secret,  rol):
        self.id = id
        self.login_email = login_email
        self.passw = passw
        self.secret = secret
        self.rol = rol

    @classmethod  
    def login(cls, login_email, passw):
        #print("@#@#@ ENTRADA login",login_email, passw)
        try:
            conn = sqlite3.connect(DATABASE)
            #print("Conexión establecida correctamente.")

            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE login_email=?", (login_email,))

            result = c.fetchone()
            #print("@#@#@ RESULT",result)

            if result and result[2] == passw:  # Verificar si se encontró el usuario y la contraseña coincide
                secret= str(datetime.now().timestamp())
                print("@#@#@ SECRET",secret, "@#@#@ SECRETstr",str(secret))
              
                user = {
                    "id": result[0],
                    "login_email": result[1],
                    "passw": result[2],
                    "secret": secret,
                    "rol": result[4]
                }
                token= Users.generate_token(user, secret)
                return user, token
            else:
                return ({"error": "Credenciales inválidas"}), 401

        except sqlite3.Error as e:
            return ({"SQLError": str(e)}, 500)
        finally:
            conn.close()

    @classmethod
    def generate_token(cls, user, secret):
        token = jwt.encode({"email": user["login_email"], "passw": user["passw"], "secret": user["secret"], "rol": user["rol"]}, secret)
        return token.decode('utf-8')
    
    @classmethod
    def create_table(cls):
        # Conexión a la base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute(''' CREATE TABLE IF NOT EXISTS 
            "users" (
                "id" INTEGER NOT NULL UNIQUE,
                 "login_email"	TEXT NOT NULL, 
                 "passw"	TEXT, 
                 "secret" TEXT,
                 "rol"	TEXT NOT NULL,
                 PRIMARY KEY("id" AUTOINCREMENT)
                );'''
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            conn.close()
    

    @classmethod
    @token_required
    def post_user(cls, user):
        try:
            conn = sqlite3.connect(DATABASE)
            #print("Conexión establecida correctamente.")

            c = conn.cursor()
            c.execute('''INSERT INTO users (login_email, passw, secret, rol)
                        VALUES (?, ?, ?, ?)''',
                    (user["login_email"], user["passw"], user["secret"], user["rol"]))
            conn.commit()
            return jsonify({'message': 'user created successfully'}), 200
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()


    @classmethod
    @token_required
    def get_user_by_id(cls, user_id):
        try:
            conn = sqlite3.connect(DATABASE)
            #print("Conexión establecida correctamente.")

            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            result = c.fetchone()
            if result:
                user = {
                    "id": result[0],
                    "login_email": result[1],
                    "passw": result[2],
                    "secret": result[3],
                    "rol": result[4]
                }
                return user
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()


    @classmethod
    @token_required
    def get_all_users(cls):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            results = c.fetchall()
            users = []
            for result in results:
                user = {
                    "id": result[0],
                    "login_email": result[1],
                    "passw": result[2],
                    "secret": result[3],
                    "rol": result[4]
                }
                users.append(user)
            return users
        
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()


    @classmethod
    @token_required
    def put_user(cls, data, user_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute('''UPDATE users SET login_email=?, passw=?, secret=?, rol=? WHERE id=?''',
                    (data['login_email'], data['passw'], data['secret'], data['rol'], user_id))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()


    @classmethod
    @token_required
    def delete_user(cls, user_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id=?", (user_id,))
            #print("Enviado SQLite")
            conn.commit()
        except sqlite3.Error as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            conn.close()


    @classmethod
    @token_required
    def patch_user(cls, data, user_id):
        conn = sqlite3.connect(DATABASE)
        try:
            c = conn.cursor()
            update_query = "UPDATE users SET "
            params = []
            for key, value in data.items():
                update_query += f"{key}=?, "
                params.append(value)
            update_query = update_query[:-2]  # Eliminar la coma y el espacio extra al final
            update_query += " WHERE id=?"
            params.append(user_id)
            c.execute(update_query, tuple(params))
            conn.commit()
            return None  # Sin errores, no se devuelve nada
        except sqlite3.Error as e:
            return str(e)  # Devuelve el mensaje de error como una cadena
        finally:
            conn.close()

