import sqlite3
import hashlib

# hash para contraseñas :)
def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


def create_database():

    conn = sqlite3.connect('cat_cafe.db', check_same_thread=False)
    cursor = conn.cursor()
    
    #  tablas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        contraseña TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ruta_foto TEXT NOT NULL,
        descripcion TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS platillos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        descripcion TEXT,
        categoria TEXT
    )
    ''')
    
    #  datos de ejemplo
    
    usuarios = [
        ('usuario_admin', hash_password('admin123')),
        ('usuario1', hash_password('pass1234')),
        ('usuario2', hash_password('securepass')),
        ('usuario4', hash_password('pass_test')),
        ('usuario5', hash_password('password1234'))
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO usuarios (usuario, contraseña) VALUES (?, ?)', usuarios)
    
    
    gatos = [
        ('Michi', 'michi.jpg', 'Aunque no lo creas, sí, así se llama, digamos que el dueño del lugar no fue muy creativo al nombrarlo, ya que cuando este amigo llego con nosotros, este establecimiento apenas estaba empezando, es el abuelito que todos quieren.'),
        ('Centauri', 'flopa.jpg', 'Técnicamente, Centauri no es un gato, pero aun así lo queremos y es muy tranquilo.'),
        ('Goobert', 'goob.jpg', 'Simplemente Goobert, existe y ya, ningun pensamiento pasa por su cabeza (aunque creemos que es capaz de colapsar el gobierno).'),
        ('Andromeda', 'andromeda.jpg', 'Andrómeda está siempre muy cerca de ti, es simplemente alguien curiosa a sus 2 años que puede pasar un tiempo divertido y lleno de actividades .'),
        ('Milky-Way', 'milky.jpg', 'Milky-way, la verdad es que es tu mejor compañero si lo que te encanta destruir cosas, según nuestros contadores ya debe 2000 en gastos de juguetes.')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO gatos (nombre, ruta_foto, descripcion) VALUES (?, ?, ?)', gatos)
    
    
    platillos = [
        ('Café Latte', 60.00, 'Espresso con leche caliente y una pequeña capa de espuma', 'Bebidas'),
        ('Pastel de Chocolate', 90.00, 'Pastel de chocolate con decoración de huella de gato', 'Postres'),
        ('pasta a pomodoro', 120.00, 'Pasta de su eleccion preparada en salsa pomodoro', 'Comidas'),
        ('Jugo de carne', 150.00, 'Plato grande de jugo de carne acompañado de tostadas de tuetano', 'Comidas'),
        ('Té Chai', 40.00, 'Té negro con especias y leche', 'Bebidas'),
        ('Galletas Galacticas', 60.00, 'Galletas caseras de mantequilla ', 'Snacks'),
        ('Meow-chiato', 60, 'Machiato con espuma decorada', 'Bebidas'),
        ('Alimenta a los patrones', 100, 'Plato de comida a base de croquetas y salmon calientito', 'alimento para gatos')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO platillos (nombre, precio, descripcion, categoria) VALUES (?, ?, ?, ?)', platillos)
    
  
 
    conn.commit() 
    conn.close()



def validar_usuario(usuario, contraseña):
    conn = sqlite3.connect('cat_cafe.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT contraseña FROM usuarios WHERE usuario = ?', (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado and resultado[0] == hash_password(contraseña):
        return True
    else:
        return False


def obtener_gatos():
    conn = sqlite3.connect('cat_cafe.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM gatos')
    gatos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return gatos


def obtener_menu():
    conn = sqlite3.connect('cat_cafe.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM platillos')
    platillos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return platillos


def obtener_imagen_gato(id_gato):
    conn = sqlite3.connect('cat_cafe.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT ruta_foto FROM gatos WHERE id = ?', (id_gato,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return resultado[0]
    else:
        return None


#lil test :D
if __name__ == '__main__':

    create_database()
    
    print("Validación de usuario admin:", validar_usuario("admin", "admin123"))
    print("Lista de gatos:", obtener_gatos())
    print("Menú completo:", obtener_menu())
