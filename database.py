import sqlite3

def conectar():
    return sqlite3.connect("mi_base.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        edad INTEGER
    )
    """)

    conn.commit()
    conn.close()


# 👇 ESTO SIEMPRE VA AL FINAL
if __name__ == "__main__":
    crear_tabla()
    print("Base de datos creada correctamente")