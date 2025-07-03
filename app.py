import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer configuración
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT", 5432))
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
databases = [db.strip() for db in os.getenv("DB_NAMES", "").split(",") if db.strip()]

# MULTIQUERY: escribe aquí tus sentencias separadas por punto y coma
multiquery = """
    alter table softqs_descarga_polizas add column doc_avant2 character(24) COLLATE pg_catalog."default"; 
"""

# Ejecutar queries en cada base de datos
for db in databases:
    print(f"Conectando a la base de datos: {db}")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=db,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # Ejecutar múltiples sentencias
        for statement in multiquery.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt + ";")
        
        conn.commit()
        print(f"✔️ Sentencias ejecutadas en {db}")
    except Exception as e:
        print(f"❌ Error en {db}: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
