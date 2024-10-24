import sqlite3

def crear_tabla_usuarios():
    conn = sqlite3.connect('mensajeria.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER,
            telefono TEXT
        )
    ''')
    conn.commit()
    conn.close()

crear_tabla_usuarios()
