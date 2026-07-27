import sqlite3
import os
from datetime import datetime

# ============================================================
# CONFIGURACIÓN DE SQLITE (BASE DE DATOS LOCAL)
# ============================================================
DB_NAME = "ofertas_cr.db"

def get_connection():
    """Crea y devuelve una conexión a SQLite"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    """Crea las tablas necesarias si no existen"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Crear tabla de tiendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            url_base TEXT NOT NULL,
            tipo_extraccion TEXT DEFAULT 'scraping_html',
            activa INTEGER DEFAULT 1,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_fabricante TEXT UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT,
            descripcion TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla de precios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS precios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            tienda_id INTEGER NOT NULL,
            precio_actual REAL NOT NULL,
            precio_regular REAL,
            porcentaje_descuento INTEGER,
            fecha_extraccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            es_oferta INTEGER DEFAULT 0,
            url_producto TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE,
            FOREIGN KEY (tienda_id) REFERENCES tiendas (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente")

def insertar_datos_prueba():
    """Inserta datos de prueba"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insertar tienda
    cursor.execute('''
        INSERT OR IGNORE INTO tiendas (nombre, url_base) 
        VALUES ('ekono', 'https://www.ekono.co.cr')
    ''')
    
    # Insertar producto
    cursor.execute('''
        INSERT OR IGNORE INTO productos (nombre, codigo_fabricante, categoria) 
        VALUES ('Microondas Samsung Prueba', 'TEST-001', 'Electrodomésticos')
    ''')
    
    # Obtener IDs
    cursor.execute("SELECT id FROM tiendas WHERE nombre = 'ekono'")
    tienda_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM productos WHERE codigo_fabricante = 'TEST-001'")
    producto_id = cursor.fetchone()[0]
    
    # Insertar precio
    cursor.execute('''
        INSERT INTO precios (producto_id, tienda_id, precio_actual, precio_regular, porcentaje_descuento, es_oferta)
        VALUES (?, ?, 95000, 120000, 21, 1)
    ''', (producto_id, tienda_id))
    
    conn.commit()
    conn.close()
    print("✅ Datos de prueba insertados correctamente")

def mostrar_datos():
    """Muestra los datos guardados"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            p.nombre as producto,
            t.nombre as tienda,
            pr.precio_actual,
            pr.precio_regular,
            pr.porcentaje_descuento,
            pr.es_oferta
        FROM precios pr
        JOIN productos p ON pr.producto_id = p.id
        JOIN tiendas t ON pr.tienda_id = t.id
    ''')
    
    datos = cursor.fetchall()
    conn.close()
    
    if datos:
        print("\n" + "=" * 60)
        print("✅ ¡DATOS VERIFICADOS CORRECTAMENTE!")
        print("=" * 60)
        for row in datos:
            print(f"   Producto: {row['producto']}")
            print(f"   Tienda: {row['tienda']}")
            print(f"   Precio actual: ₡{row['precio_actual']:,.2f}")
            print(f"   Precio regular: ₡{row['precio_regular']:,.2f}")
            print(f"   Descuento: {row['porcentaje_descuento']}%")
            print(f"   Es oferta: {'Sí' if row['es_oferta'] else 'No'}")
            print("-" * 40)
        print("=" * 60)
    else:
        print("❌ No se encontraron datos")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA CON SQLITE")
    print("📦 Creando base de datos local...")
    crear_tablas()
    print("📝 Insertando datos de prueba...")
    insertar_datos_prueba()
    mostrar_datos()
    print(f"\n✅ Prueba completada. Base de datos guardada en: {DB_NAME}")
