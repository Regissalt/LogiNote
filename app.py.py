import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_cyberpunk_aqui'

DATABASE = 'loginote.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            nota1 REAL,
            nota2 REAL,
            nota3 REAL,
            promedio REAL,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    if 'user_id' in session:
        conn = get_db_connection()
        materias = conn.execute('SELECT * FROM materias WHERE user_id = ?', (session['user_id'],)).fetchall()
        conn.close()
        return render_template('index.html', usuario=session['username'], materias=materias)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO usuarios (usuario, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            flash('¡Cuenta creada con éxito! Ya podés iniciar sesión.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Ese nombre de usuario ya está registrado.')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE usuario = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['usuario']
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/calcular', methods=['POST'])
def calcular():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    materia = request.form['materia']
    n1 = float(request.form['nota1'])
    n2 = request.form['nota2']
    n3 = request.form['nota3']
    
    n2 = float(n2) if n2 else 0.0
    n3 = float(n3) if n3 else 0.0
    
    divisores = 1 + (1 if n2 > 0 else 0) + (1 if n3 > 0 else 0)
    promedio = round((n1 + n2 + n3) / divisores, 2)
    
    if n1 == 7.50:
        mensaje = "¡Nivel Dios activado! El 7.50 de la victoria automatizada."
        color = "#00ff88"
    elif promedio >= 6.0:
        mensaje = "Vas bien encaminado, meta alcanzada."
        color = "#00ff88"
    else:
        mensaje = "Alerta: Necesitás meterle pata en el próximo trimestre."
        color = "#ff3e3e"
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO materias (user_id, nombre, nota1, nota2, nota3, promedio)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], materia, n1, request.form['nota2'] or None, request.form['nota3'] or None, promedio))
    conn.commit()
    conn.close()
    
    return render_template('resultados.html', materia=materia, promedio=promedio, mensaje=mensaje, color_texto=color) 

