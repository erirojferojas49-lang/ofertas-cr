"""
PRUEBA COMPLETA DEL SISTEMA - VERSIÓN CON URL DIRECTA
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ============================================================
# URL DE SUPABASE - ESCRITA DIRECTAMENTE AQUÍ
# ============================================================
SUPABASE_URL = "postgresql://postgres:mzx7ywCwZzehzqMfA@db.ynciugrecldpgrnklazq.supabase.co:5432/postgres"

print("=" * 60)
print("🚀 INICIANDO PRUEBA DEL SISTEMA OFERTAS CR")
print("=" * 60)

# ============================================================
# CONECTAR A SUPABASE
# ============================================================
print("\n📡 Conectando a Supabase...")

try:
    # Crear el motor de SQLAlchemy
    engine = create_engine(SUPABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    print("✅ Conexión exitosa a Supabase")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    sys.exit(1)

# ============================================================
# VERIFICAR TIENDA 'ekono'
# ============================================================
print("\n🏪 Verificando tienda 'ekono'...")

try:
    # Verificar si la tienda existe
    result = session.execute(text("SELECT id FROM tiendas WHERE nombre = 'ekono'"))
    tienda = result.fetchone()
    
    if tienda:
        tienda_id = tienda[0]
        print(f"✅ Tienda 'ekono' encontrada con ID: {tienda_id}")
    else:
        print("⚠️ Tienda 'ekono' no encontrada. Creándola...")
        session.execute(
            text("INSERT INTO tiendas (nombre, url_base, tipo_extraccion) VALUES ('ekono', 'https://www.ekono.co.cr', 'scraping_html')")
        )
        session.commit()
        print("✅ Tienda 'ekono' creada exitosamente")
        
        result = session.execute(text("SELECT id FROM tiendas WHERE nombre = 'ekono'"))
        tienda_id = result.fetchone()[0]
except Exception as e:
    print(f"❌ Error verificando tienda: {e}")
    session.rollback()
    sys.exit(1)

# ============================================================
# CREAR PRODUCTO DE PRUEBA
# ============================================================
print("\n📦 Creando producto de prueba...")

try:
    # Verificar si el producto ya existe
    result = session.execute(
        text("SELECT id FROM productos WHERE codigo_fabricante = 'TEST-001'")
    )
    producto = result.fetchone()
    
    if producto:
        producto_id = producto[0]
        print(f"⚠️ Producto de prueba ya existe con ID: {producto_id}")
    else:
        session.execute(
            text("""
                INSERT INTO productos (nombre, codigo_fabricante, categoria, descripcion)
                VALUES ('Microondas Samsung Prueba', 'TEST-001', 'Electrodomésticos', 'Producto de prueba')
            """)
        )
        session.commit()
        print("✅ Producto de prueba creado exitosamente")
        
        result = session.execute(
            text("SELECT id FROM productos WHERE codigo_fabricante = 'TEST-001'")
        )
        producto_id = result.fetchone()[0]
except Exception as e:
    print(f"❌ Error creando producto: {e}")
    session.rollback()
    sys.exit(1)

# ============================================================
# GUARDAR PRECIO DE PRUEBA
# ============================================================
print("\n💰 Guardando precio de prueba...")

try:
    # Verificar si ya existe un precio
    result = session.execute(
        text("""
            SELECT id FROM precios 
            WHERE producto_id = :producto_id AND tienda_id = :tienda_id
        """),
        {"producto_id": producto_id, "tienda_id": tienda_id}
    )
    precio = result.fetchone()
    
    if precio:
        print(f"⚠️ Precio ya existe. Actualizando...")
        session.execute(
            text("""
                UPDATE precios 
                SET precio_actual = 95000, 
                    precio_regular = 120000, 
                    porcentaje_descuento = 21,
                    es_oferta = true,
                    fecha_extraccion = CURRENT_TIMESTAMP
                WHERE producto_id = :producto_id AND tienda_id = :tienda_id
            """),
            {"producto_id": producto_id, "tienda_id": tienda_id}
        )
        session.commit()
        print("✅ Precio actualizado exitosamente")
    else:
        session.execute(
            text("""
                INSERT INTO precios (producto_id, tienda_id, precio_actual, precio_regular, porcentaje_descuento, es_oferta)
                VALUES (:producto_id, :tienda_id, 95000, 120000, 21, true)
            """),
            {"producto_id": producto_id, "tienda_id": tienda_id}
        )
        session.commit()
        print("✅ Precio guardado exitosamente")
except Exception as e:
    print(f"❌ Error guardando precio: {e}")
    session.rollback()
    sys.exit(1)

# ============================================================
# VERIFICAR DATOS GUARDADOS
# ============================================================
print("\n🔍 Verificando datos guardados...")

try:
    result = session.execute(
        text("""
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
            WHERE pr.producto_id = :producto_id
        """),
        {"producto_id": producto_id}
    )
    datos = result.fetchone()
    
    if datos:
        print("\n" + "=" * 60)
        print("✅ ¡DATOS VERIFICADOS CORRECTAMENTE!")
        print("=" * 60)
        print(f"   Producto: {datos[0]}")
        print(f"   Tienda: {datos[1]}")
        print(f"   Precio actual: ₡{datos[2]:,.2f}")
        print(f"   Precio regular: ₡{datos[3]:,.2f}")
        print(f"   Descuento: {datos[4]}%")
        print(f"   Es oferta: {datos[5]}")
        print("=" * 60)
    else:
        print("❌ No se encontraron datos")
except Exception as e:
    print(f"❌ Error verificando datos: {e}")

# ============================================================
# FINALIZAR
# ============================================================
session.close()
print("\n✅ PRUEBA COMPLETADA EXITOSAMENTE!")
print("🎉 El sistema está listo para usar.")
