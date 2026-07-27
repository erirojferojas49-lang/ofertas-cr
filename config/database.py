import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_db_connection():
    """Establece conexión con Supabase"""
    try:
        url = os.getenv("SUPABASE_URL")
        if not url:
            raise ValueError("❌ SUPABASE_URL no está definida en .env")
        
        conn = psycopg2.connect(url)
        print("✅ Conexión a Supabase exitosa")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        return None

def test_connection():
    """Prueba simple para verificar la conexión"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"📦 PostgreSQL versión: {version[0]}")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error en la consulta: {e}")

if __name__ == "__main__":
    test_connection()
