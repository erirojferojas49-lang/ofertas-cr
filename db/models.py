from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Tienda(Base):
    __tablename__ = 'tiendas'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    url_base = Column(String(255), nullable=False)
    tipo_extraccion = Column(String(20), default='scraping_html')
    activa = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.now)

class Producto(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True)
    codigo_fabricante = Column(String(100), unique=True, nullable=True)
    nombre = Column(String(255), nullable=False)
    categoria = Column(String(100))
    descripcion = Column(Text)
    fecha_registro = Column(DateTime, default=datetime.now)

class Precio(Base):
    __tablename__ = 'precios'
    
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    tienda_id = Column(Integer, ForeignKey('tiendas.id'))
    precio_actual = Column(Float, nullable=False)
    precio_regular = Column(Float)
    porcentaje_descuento = Column(Integer)
    fecha_extraccion = Column(DateTime, default=datetime.now)
    es_oferta = Column(Boolean, default=False)
    url_producto = Column(String(500))
