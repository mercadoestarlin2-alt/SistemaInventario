from flask import Flask, render_template, request, redirect, url_for, session, flash
import database

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones' # Necesario para manejar login

# Inicializar Base de Datos al arrancar
database.inicializar_bd()

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# --- MÓDULO 1: GESTIÓN DE USUARIOS (LOGIN) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        conexion = database.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado:
            session['usuario'] = usuario
            session['rol'] = resultado[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- MÓDULO 2: GESTIÓN DE INVENTARIO (DASHBOARD) ---
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    conexion = database.conectar()
    cursor = conexion.cursor()
    
    # Si el Admin agrega un producto nuevo
    if request.method == 'POST' and session['rol'] == 'Administrador':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)", (nombre, descripcion, precio))
        conexion.commit()
        flash('Producto agregado con éxito', 'success')
        return redirect(url_for('dashboard'))

    # Obtener todos los productos para listarlos
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    
    return render_template('dashboard.html', productos=productos)

# --- MÓDULO 3: MOVIMIENTOS DE STOCK ---
@app.route('/movimiento', methods=['GET', 'POST'])
def movimiento():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    conexion = database.conectar()
    cursor = conexion.cursor()
    
    if request.method == 'POST':
        prod_id = int(request.form['producto_id'])
        tipo = request.form['tipo']
        cantidad = int(request.form['cantidad'])
        
        cursor.execute("SELECT cantidad FROM productos WHERE id = ?", (prod_id,))
        producto = cursor.fetchone()
        
        if producto:
            stock_actual = producto[0]
            if tipo == 'SALIDA' and stock_actual < cantidad:
                flash('Error: Stock insuficiente para esta salida.', 'danger')
            else:
                nuevo_stock = stock_actual + cantidad if tipo == 'ENTRADA' else stock_actual - cantidad
                cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nuevo_stock, prod_id))
                flash(f'Movimiento de {tipo} registrado correctamente.', 'success')
                conexion.commit()
        else:
            flash('El producto no existe.', 'danger')
            
    cursor.execute("SELECT id, nombre FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return render_template('movimiento.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)