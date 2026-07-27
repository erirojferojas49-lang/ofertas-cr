"""
Prueba completa del sistema Ofertas CR
Este script verifica que todos los componentes funcionan correctamente
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importar nuestros módulos
from db.models import Producto, Precio, Tienda
from db.queries import guardar_producto, guardar_precio, get_session
from config.database import test_connection

def crear_datos_prueba():
    """Crea un producto y un precio de prueba"""
    
    print("🚀 Iniciando prueba del sistema...")
    
    # 1. Probar conexión a Supabase
    print("\n📡 Probando conexión a Supabase...")
    test_connection()
    
    # 2. Crear sesión
    session = get_session()
    
    # 3. Verificar que la tienda existe
    print("\n🏪 Verificando tiendas...")
    tienda = session.query(Tienda).filter(Tienda.nombre == "ekono").first()
    if not tienda:
        print("❌ La tienda 'ekono' no existe. Creándola...")
        tienda = Tienda(
            nombre="ekono",
            url_base="https://www.ekono.co.cr",
            tipo_extraccion="scraping_html"
        )
        session.add(tienda)
        session.commit()
        print(f"✅ Tienda 'ekono' creada con ID: {tienda.id}")
    else:
        print(f"✅ Tienda 'ekono' encontrada con ID: {tienda.id}")
    
    # 4. Crear un producto de prueba
    print("\n📦 Creando producto de prueba...")
    producto = Producto(
        nombre="Microondas Samsung Prueba",
        codigo_fabricante="TEST-001",
        categoria="Electrodomésticos",
        descripcion="Producto de prueba para verificar el sistema"
    )
    session.add(producto)
    session.commit()
    print(f"✅ Producto creado con ID: {producto.id}")
    
    # 5. Guardar un precio para el producto
    print("\n💰 Guardando precio de prueba...")
    precio = Precio(
        producto_id=producto.id,
        tienda_id=tienda.id,
        precio_actual=95000.00,
        precio_regular=120000.00,
        porcentaje_descuento=21,
        es_oferta=True,
        url_producto="https://www.ekono.co.cr/producto-test"
    )
    session.add(precio)
    session.commit()
    print(f"✅ Precio guardado con ID: {precio.id}")
    
    # 6. Verificar que se guardó correctamente
    print("\n🔍 Verificando datos guardados...")
    producto_guardado = session.query(Producto).filter(Producto.id == producto.id).first()
    precio_guardado = session.query(Precio).filter(Precio.producto_id == producto.id).first()
    
    if producto_guardado and precio_guardado:
        print("✅ ¡DATOS VERIFICADOS CORRECTAMENTE!")
        print(f"   Producto: {producto_guardado.nombre}")
        print(f"   Precio actual: ₡{precio_guardado.precio_actual:,.2f}")
        print(f"   Precio regular: ₡{precio_guardado.precio_regular:,.2f}")
        print(f"   Descuento: {precio_guardado.porcentaje_descuento}%")
        print(f"   Es oferta: {precio_guardado.es_oferta}")
    else:
        print("❌ Error: No se pudieron recuperar los datos")
    
    # 7. Cerrar sesión
    session.close()
    print("\n✅ Prueba completada exitosamente!")

if __name__ == "__main__":
    crear_datos_prueba()
