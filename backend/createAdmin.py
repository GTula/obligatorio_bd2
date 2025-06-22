import re
import bcrypt
from db import get_db_connection

def validar_password(password):
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return "La contraseña debe tener al menos una letra mayúscula."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return "La contraseña debe tener al menos un símbolo."
    return None

def crear_usuario_admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        usuario = input("Ingrese el nombre de usuario: ").strip()
        cursor.execute("SELECT * FROM administrador WHERE usuario = %s", (usuario,))
        if cursor.fetchone():
            print("Ya existe un administrador con ese nombre de usuario.")
            return

        while True:
            password = input("Ingrese la contraseña: ").strip()
            confirm = input("Confirme la contraseña: ").strip()

            if password != confirm:
                print("Las contraseñas no coinciden.")
                continue

            error = validar_password(password)
            if error:
                print(f"{error}")
            else:
                break

        # Hashear la contraseña
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insertar en la base de datos
        cursor.execute(
            "INSERT INTO administrador (usuario, password) VALUES (%s, %s)",
            (usuario, password_hash)
        )
        conn.commit()
        print("Administrador creado con éxito.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_usuario_admin()
