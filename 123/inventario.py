import database

def agregar_producto():
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    precio = float(input("Precio: "))
    
    conexion = database.conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)", (nombre, descripcion, precio))
    conexion.commit()
    conexion.close()
    print("Producto agregado con éxito.")

def listar_productos():
    print("\n--- INVENTARIO ACTUAL ---")
    conexion = database.conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    
    if not productos:
        print("No hay productos en el inventario.")
        return
        
    print(f"{'ID':<5} | {'Nombre':<20} | {'Stock':<8} | {'Precio':<10}")
    print("-" * 50)
    for p in productos:
        print(f"{p[0]:<5} | {p[1]:<20} | {p[3]:<8} | ${p[4]:<10.2f}")