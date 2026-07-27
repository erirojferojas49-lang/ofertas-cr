from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Tienda, Producto, Precio
import os

def get_session():
    url = os.getenv("SUPABASE_URL")
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()

def guardar_producto(session, nombre, codigo_fabricante=None, categoria=None):
    producto = Producto(
        nombre=nombre,
        codigo_fabricante=codigo_fabricante,
        categoria=categoria
    )
    session.add(producto)
    session.commit()
    return producto

def guardar_precio(session, producto_id, tienda_id, precio_actual, precio_regular=None, url_producto=None):
    descuento = None
    es_oferta = False
    if precio_regular and precio_actual < precio_regular:
        descuento = int(((precio_regular - precio_actual) / precio_regular) * 100)
        es_oferta = True
    
    precio = Precio(
        producto_id=producto_id,
        tienda_id=tienda_id,
        precio_actual=precio_actual,
        precio_regular=precio_regular,
        porcentaje_descuento=descuento,
        es_oferta=es_oferta,
        url_producto=url_producto
    )
    session.add(precio)
    session.commit()
    return precio
