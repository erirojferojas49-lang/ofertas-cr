#!/bin/bash
echo "🔧 Instalando dependencias para Ofertas CR..."

# Actualizar pip
python -m pip install --upgrade pip

# Instalar todos los paquetes
python -m pip install python-dotenv psycopg2-binary sqlalchemy streamlit beautifulsoup4 requests pandas plotly

echo ""
echo "✅ Verificando instalación..."
python -c "import dotenv, psycopg2, sqlalchemy; print('✅ Todos los paquetes instalados correctamente')"

echo ""
echo "🚀 Sistema listo! Ejecuta: python test_sistema.py"
