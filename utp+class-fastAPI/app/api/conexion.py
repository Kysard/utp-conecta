from fastapi import APIRouter, HTTPException
import pyodbc

router = APIRouter()

# Configuración de la conexión (ajusta estos valores según tu entorno)
DB_CONFIG = {
    'server': 'localhost',
    'database': 'UTPConecta',
    'username': 'UtpConecta',
    'password': 'Utp2025*BD',
    'port': '52743'
}

def get_db_connection():
    """Función para establecer conexión con la base de datos"""
    try:
        connection_string = f'DRIVER={{SQL Server}};SERVER={DB_CONFIG["server"]},{DB_CONFIG["port"]};DATABASE={DB_CONFIG["database"]};UID={DB_CONFIG["username"]};PWD={DB_CONFIG["password"]}'
        connection = pyodbc.connect(connection_string)
        return connection
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión a la base de datos: {str(e)}"
        )

@router.get("/test")
def probar_conexion():
    """Endpoint simple para probar la conexión a la base de datos"""
    try:
        conn = get_db_connection()
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test_connection")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "message": "Conexión a la base de datos exitosa",
            "test_result": result.test_connection
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al probar la conexión: {str(e)}"
        )