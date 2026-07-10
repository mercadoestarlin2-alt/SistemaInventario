import sqlite3

def conectar():
    return sqlite3.connect("inventario.db")

def inicializar_bd():
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER DEFAULT 0,
            precio REAL NOT NULL
        )
    ''')
    
    try:
        cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)", 
                       ('admin', 'admin123', 'Administrador'))
        cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)", 
                       ('empleado', '1234', 'Empleado'))
    except sqlite3.IntegrityError:
        pass
        
    conexion.commit()
    conexion.close()