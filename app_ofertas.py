"""
🐋 OFERTAS CR - BUSCADOR DE OFERTAS PARA EL DÍA DE LA MADRE
Sistema ligero para detectar promociones en tiendas de Costa Rica.
Basado en la arquitectura de Sakura V5.
"""

import os
import re
import requests
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================
# CONFIGURACIÓN DE OFERTAS
# ============================================================

# Fuentes de datos (RSS de tiendas o URLs de páginas de ofertas)
FUENTES = [
    {
        "nombre": "Walmart Costa Rica",
        "url": "https://www.walmart.co.cr/ofertas",
        "tipo": "web"
    },
    {
        "nombre": "Pricesmart Costa Rica",
        "url": "https://www.pricesmart.co.cr/ofertas",
        "tipo": "web"
    },
    {
        "nombre": "Universal Costa Rica",
        "url": "https://www.universal.co.cr/ofertas",
        "tipo": "web"
    },
    {
        "nombre": "Monge Costa Rica",
        "url": "https://www.monge.co.cr/ofertas",
        "tipo": "web"
    }
]

# Palabras clave para detectar ofertas
PALABRAS_CLAVE = [
    "descuento", "promoción", "rebaja", "2x1", "liquidación",
    "oferta", "cyber", "black friday", "día de la madre",
    "precio especial", "paquete", "combo", "ganga"
]

# ============================================================
# FUNCIONES DE DETECCIÓN DE OFERTAS
# ============================================================

def buscar_ofertas_en_texto(texto: str) -> List[Dict]:
    """
    Busca ofertas en un texto usando palabras clave y expresiones regulares.
    """
    ofertas = []
    texto_lower = texto.lower()
    
    # Buscar patrones de precios (ej. "₡10,000", "$10.99")
    patron_precio = re.compile(r'(?P<moneda>₡|\$)\s*(?P<monto>[\d,]+\.?\d*)')
    
    for palabra in PALABRAS_CLAVE:
        if palabra in texto_lower:
            # Buscar precios en el texto
            precios = patron_precio.findall(texto)
            ofertas.append({
                "palabra_clave": palabra,
                "precios": [f"{p[0]}{p[1]}" for p in precios[:3]],
                "fragmento": texto[:200]
            })
    
    return ofertas

def buscar_ofertas_en_fuente(fuente: Dict) -> List[Dict]:
    """
    Busca ofertas en una fuente específica (web o RSS).
    """
    try:
        # Simulación de scraping (en la práctica, usarías requests + BeautifulSoup)
        # Por ahora, generamos datos de ejemplo
        print(f"🔍 Buscando en {fuente['nombre']}...")
        
        # Datos de ejemplo (reemplazar con scraping real)
        ofertas_ejemplo = [
            {
                "fuente": fuente['nombre'],
                "titulo": f"Oferta en {fuente['nombre']} - Día de la Madre",
                "descripcion": "Aprovecha descuentos en electrodomésticos, ropa y más.",
                "precio_original": "₡50,000",
                "precio_oferta": "₡35,000",
                "descuento": "30%",
                "url": fuente['url'],
                "fecha_deteccion": datetime.now().isoformat()
            }
        ]
        return ofertas_ejemplo
    except Exception as e:
        print(f"⚠️ Error en {fuente['nombre']}: {e}")
        return []

# ============================================================
# DASHBOARD DE OFERTAS (VERSIÓN TEXTO)
# ============================================================

def mostrar_ofertas(ofertas: List[Dict]):
    """
    Muestra las ofertas en formato legible.
    """
    if not ofertas:
        print("❌ No se encontraron ofertas.")
        return
    
    print("\n🐋 OFERTAS CR - RESULTADOS")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    for i, oferta in enumerate(ofertas[:10], 1):
        print(f"\n🔹 OFERTA #{i}")
        print(f"   🏬 Tienda: {oferta.get('fuente', 'Desconocida')}")
        print(f"   📝 Producto: {oferta.get('titulo', 'N/A')}")
        print(f"   💰 Precio original: {oferta.get('precio_original', 'N/A')}")
        print(f"   💸 Precio oferta: {oferta.get('precio_oferta', 'N/A')}")
        print(f"   🎯 Descuento: {oferta.get('descuento', 'N/A')}")
        print(f"   🔗 URL: {oferta.get('url', '#')}")

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    print("🐋 OFERTAS CR - BUSCADOR DE OFERTAS PARA EL DÍA DE LA MADRE")
    print("=" * 60)
    
    todas_ofertas = []
    
    for fuente in FUENTES:
        ofertas = buscar_ofertas_en_fuente(fuente)
        todas_ofertas.extend(ofertas)
    
    mostrar_ofertas(todas_ofertas)
    
    print("\n" + "=" * 60)
    print("✅ Búsqueda completada. ¡Feliz Día de la Madre!")

if __name__ == "__main__":
    main()
