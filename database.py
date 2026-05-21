import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("mi_base.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL CHECK (edad > 0),
        fecha TEXT
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_nombre ON usuarios(nombre)
    """)

    conn.commit()
    conn.close()

def agregar_usuario(nombre, edad):
    conn = conectar()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
    INSERT INTO usuarios (nombre, edad, fecha)
    VALUES (?, ?, ?)
    """, (nombre, edad, fecha))

    conn.commit()
    conn.close()

def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()

    conn.close()
    return datos

if __name__ == "__main__":
    crear_tabla()
    print("Base de datos lista")
